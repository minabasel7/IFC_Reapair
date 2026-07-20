import ifcopenshell
import requests
import time
import subprocess
import sys
import os

API_URL = "http://127.0.0.1:8000/api/process"
DOWNLOAD_URL_BASE = "http://127.0.0.1:8000"

def inspect_model(filename):
    print(f"\\n--- Inspecting {filename} ---")
    try:
        model = ifcopenshell.open(filename)
        schema = model.schema
        apps = model.by_type('IfcApplication')
        app_name = apps[0].ApplicationFullName if apps else 'Unknown Application'
        entities = len(model.by_type("IfcRoot"))
        print(f"Schema: {schema}")
        print(f"Application: {app_name}")
        print(f"Entities (IfcRoot): {entities}")
    except Exception as e:
        print(f"Failed to inspect {filename}: {e}")

def test_model(filename):
    print(f"\\n--- Testing {filename} via API ---")
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"File Size: {size_mb:.2f} MB")
    
    with open(filename, "rb") as f:
        files = {"file": (filename, f, "application/octet-stream")}
        t0 = time.time()
        resp = requests.post(API_URL, files=files)
        total_time = time.time() - t0
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Validation Time: {data.get('validation_time_ms')} ms")
            print(f"Repair Time: {data.get('repair_time_ms')} ms")
            print(f"Detected Issues: {data.get('detected_issues')}")
            print(f"Repaired Issues: {data.get('repairs_performed')}")
            
            d_url = data.get("download_url")
            dl_resp = requests.get(DOWNLOAD_URL_BASE + d_url)
            if dl_resp.status_code == 200:
                print("Download: Success")
                with open("temp_repaired.ifc", "wb") as temp_f:
                    temp_f.write(dl_resp.content)
                try:
                    repaired_model = ifcopenshell.open("temp_repaired.ifc")
                    print("Repaired File Opens in IfcOpenShell (Bonsai compatibility): Yes")
                    # Check geometry preservation (walls still exist)
                    walls = repaired_model.by_type("IfcWall")
                    print(f"Geometry preserved (Wall count): {len(walls)}")
                except Exception as e:
                    print(f"Repaired File Opens: No ({e})")
                finally:
                    if os.path.exists("temp_repaired.ifc"):
                        os.remove("temp_repaired.ifc")
            else:
                print("Download: Failed")
        else:
            print(f"API Failed: {resp.status_code} - {resp.text}")


if __name__ == '__main__':
    files = ['schependomlaan_arch.ifc', 'bernts_steel.ifc', 'hb_mep.ifc']
    for f in files:
        inspect_model(f)
    
    print("\\nStarting API Server...")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"])
    time.sleep(3) # Wait for startup

    try:
        for f in files:
            test_model(f)
    finally:
        print("\\nCleaning up API...")
        proc.terminate()
