import os
import time
import requests
import subprocess
import sys

API_URL = "http://127.0.0.1:8000/api/process"
DOWNLOAD_URL_BASE = "http://127.0.0.1:8000"

def generate_ifc(filename, schema="IFC2X3", count=10, error_duplicates=0, error_orphans=0):
    header = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('{filename}','2023-01-01T00:00:00',('Test'),('Test'),'IfcOpenShell','IfcOpenShell','');
FILE_SCHEMA(('{schema}'));
ENDSEC;
DATA;
#1=IFCPROJECT('0$X_X$X_X$X_X$X_X$X_X',#2,'Test Project',$,$,$,$,(#3),#4);
#2=IFCOWNERHISTORY(#5,#6,$,.ADDED.,$,$,$,1672531200);
#3=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.0E-5,#7,$);
#4=IFCUNITASSIGNMENT((#8));
#5=IFCPERSONANDORGANIZATION(#9,#10,$);
#6=IFCAPPLICATION(#10,'1.0','Test App','Test App');
#7=IFCAXIS2PLACEMENT3D(#11,#12,#13);
#8=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#9=IFCPERSON($,'Test Person',$,$,$,$,$,$);
#10=IFCORGANIZATION($,'Test Org',$,$,$);
#11=IFCCARTESIANPOINT((0.,0.,0.));
#12=IFCDIRECTION((0.,0.,1.));
#13=IFCDIRECTION((1.,0.,0.));
#14=IFCBUILDING('1$X_X$X_X$X_X$X_X$X_X',#2,'Test Building',$,$,#15,$,$,.ELEMENT.,$,$,$);
#15=IFCLOCALPLACEMENT($,#7);
#16=IFCRELAGGREGATES('2$X_X$X_X$X_X$X_X$X_X',#2,'ProjectContainer',$,#1,(#14));
"""
    body = ""
    valid_walls = []
    
    start_idx = 20
    # Generate valid walls
    for i in range(count):
        wall_id = start_idx + i
        valid_walls.append(f"#{wall_id}")
        body += f"#{wall_id}=IFCWALL('W_{i}_X$X_X$X_X$X_X$X',#2,'Wall {i}',$,$,#15,$,$);\n"
    
    start_idx += count
    
    # Generate duplicate GUID walls
    for i in range(error_duplicates):
        wall_id = start_idx + i
        valid_walls.append(f"#{wall_id}")
        body += f"#{wall_id}=IFCWALL('DUPLICATE_GUID_XXX',#2,'DupWall {i}',$,$,#15,$,$);\n"
        
    start_idx += error_duplicates
    
    # Generate orphaned elements (no spatial structure)
    for i in range(error_orphans):
        wall_id = start_idx + i
        body += f"#{wall_id}=IFCWALL('O_{i}_X$X_X$X_X$X_X$X',#2,'Orphan {i}',$,$,#15,$,$);\n"

    rel_id = start_idx + error_orphans + 1
    if valid_walls:
        body += f"#{rel_id}=IFCRELCONTAINEDINSPATIALSTRUCTURE('R_{rel_id}_X$X_X$X',#2,'Container',$,({','.join(valid_walls)}),#14);\n"
        
    footer = """ENDSEC;
END-ISO-10303-21;"""

    with open(filename, "w") as f:
        f.write(header + body + footer)

    return os.path.getsize(filename)


def run_test(name, filename):
    print(f"\\n--- Testing: {name} ---")
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"File Size: {size_mb:.2f} MB")
    
    with open(filename, "rb") as f:
        files = {"file": (filename, f, "application/octet-stream")}
        t0 = time.time()
        resp = requests.post(API_URL, files=files)
        total_time = time.time() - t0
        
        if resp.status_code == 200:
            data = resp.json()
            stats = data.get("statistics", {})
            print(f"Schema: {stats.get('schema')}")
            print(f"Entities: {stats.get('entities_count')}")
            print(f"Validation Time: {data.get('validation_time_ms')} ms")
            print(f"Repair Time: {data.get('repair_time_ms')} ms")
            print(f"Detected Issues: {data.get('detected_issues')}")
            print(f"Repaired Issues: {data.get('repairs_performed')}")
            
            d_url = data.get("download_url")
            dl_resp = requests.get(DOWNLOAD_URL_BASE + d_url)
            if dl_resp.status_code == 200:
                print("Download: Success")
                # Test opening the repaired file
                with open("temp_repaired.ifc", "wb") as temp_f:
                    temp_f.write(dl_resp.content)
                import ifcopenshell
                try:
                    repaired_model = ifcopenshell.open("temp_repaired.ifc")
                    print("Repaired File Opens: Yes")
                    # Check geometry preservation (walls still exist)
                    walls = repaired_model.by_type("IfcWall")
                    print(f"Geometry preserved (Wall count): {len(walls)}")
                except Exception as e:
                    print(f"Repaired File Opens: No ({e})")
                finally:
                    os.remove("temp_repaired.ifc")
            else:
                print("Download: Failed")
        else:
            print(f"API Failed: {resp.status_code} - {resp.text}")

def main():
    print("Generating files...")
    generate_ifc("small_2x3.ifc", schema="IFC2X3", count=100)
    generate_ifc("medium_4.ifc", schema="IFC4", count=5000)
    generate_ifc("large_4.ifc", schema="IFC4", count=25000)
    generate_ifc("no_errors.ifc", schema="IFC2X3", count=1000, error_duplicates=0, error_orphans=0)
    generate_ifc("multiple_issues.ifc", schema="IFC4", count=100, error_duplicates=50, error_orphans=50)

    # Start API
    print("Starting API Server...")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"])
    time.sleep(3) # Wait for startup

    try:
        run_test("Small Architectural IFC (IFC2X3)", "small_2x3.ifc")
        run_test("Medium Sized IFC (IFC4)", "medium_4.ifc")
        run_test("Large IFC (IFC4)", "large_4.ifc")
        run_test("IFC With No Errors", "no_errors.ifc")
        run_test("IFC With Multiple Semantic Issues", "multiple_issues.ifc")
    finally:
        print("\\nCleaning up...")
        proc.terminate()
        for f in ["small_2x3.ifc", "medium_4.ifc", "large_4.ifc", "no_errors.ifc", "multiple_issues.ifc"]:
            if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    main()
