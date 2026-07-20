import requests
import time
import sys

API_URL = "http://127.0.0.1:8000/api"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        print("Health check passed:", response.json())
    else:
        print("Health check failed:", response.status_code, response.text)
        sys.exit(1)

def test_process():
    print("Testing process endpoint...")
    with open("test.ifc", "rb") as f:
        files = {"file": ("test.ifc", f, "application/octet-stream")}
        response = requests.post(f"{API_URL}/process", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("Process passed!")
            print("Score:", data.get("validation_score"))
            print("Issues Found:", data.get("detected_issues"))
            print("Repairs Performed:", data.get("repairs_performed"))
            print("Download URL:", data.get("download_url"))
            return data.get("download_url")
        else:
            print("Process failed:", response.status_code, response.text)
            sys.exit(1)

def test_download(download_url):
    print(f"Testing download endpoint: {download_url}")
    response = requests.get(f"http://127.0.0.1:8000{download_url}")
    if response.status_code == 200:
        with open("repaired_test.ifc", "wb") as f:
            f.write(response.content)
        print("Download passed! File saved as repaired_test.ifc")
    else:
        print("Download failed:", response.status_code, response.text)
        sys.exit(1)

if __name__ == "__main__":
    # Wait a bit for server to start if running script immediately
    time.sleep(2)
    test_health()
    download_url = test_process()
    if download_url:
        test_download(download_url)
    print("All backend tests passed successfully!")
