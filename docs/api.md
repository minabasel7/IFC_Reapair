# API Documentation

The IFC Repair SaaS backend exposes a REST API powered by FastAPI.

## Base URL
When running locally: `http://localhost:8000`
In production: The API is hosted at the `/api` route of the Vercel deployment (or an external containerized URL, managed via the `NEXT_PUBLIC_API_URL` environment variable).

---

## Endpoints

### 1. Health Check
Checks if the IFC Processing Engine is online and responsive.

**Request:**
- **URL**: `/api/health`
- **Method**: `GET`

**Response:**
- **Status Code**: `200 OK`
- **Body**:
  ```json
  {
    "status": "healthy",
    "service": "IFC Repair Engine"
  }
  ```

---

### 2. Process IFC Model
Uploads an OpenBIM `.ifc` file for validation, analysis, and repair. 

**Request:**
- **URL**: `/api/process`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Payload**:
  - `file`: The `.ifc` file (must have `.ifc` extension).

**Response (Success):**
- **Status Code**: `200 OK`
- **Body**:
  ```json
  {
    "timestamp": "2026-07-20T00:00:00.000Z",
    "validation_score": 90,
    "statistics": {
      "schema": "IFC2X3",
      "entities_count": 46302
    },
    "detected_issues": 2,
    "repairs_performed": 2,
    "remaining_warnings": 0,
    "validation_time_ms": 704.0,
    "repair_time_ms": 6550.43,
    "issues_list": [],
    "download_url": "/api/download/63bd220d-003e-474c-af99-7add08e9148d_repaired.ifc"
  }
  ```

**Response (Error):**
- **Status Code**: `400 Bad Request` or `500 Internal Server Error`
- **Body**:
  ```json
  {
    "detail": "Invalid or corrupted IFC file. Could not parse."
  }
  ```

---

### 3. Download Repaired Model
Retrieves the securely repaired IFC model. The file is temporarily stored and immediately deleted securely after download (or after 10 minutes if not downloaded).

**Request:**
- **URL**: `/api/download/{file_id}`
- **Method**: `GET`
- **Parameters**:
  - `file_id`: The unique filename returned from the `/api/process` endpoint.

**Response (Success):**
- **Status Code**: `200 OK`
- **Content-Type**: `application/octet-stream`
- **Headers**:
  - `Content-Disposition`: `attachment; filename="repaired_model.ifc"`

**Response (Error):**
- **Status Code**: `404 Not Found`
- **Body**:
  ```json
  {
    "detail": "File not found or already deleted."
  }
  ```
