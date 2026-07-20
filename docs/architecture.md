# System Architecture

## 1. Project Architecture

The IFC Repair SaaS is structured as a decoupled application with a React-based frontend and a Python-based processing engine.

```mermaid
graph TD
    Client[Web Browser Client]
    VercelEdge[Vercel Edge Network]
    Frontend[Next.js Frontend React]
    Backend[Python FastAPI Backend]
    IfcLib[IfcOpenShell C++ Bindings]
    Disk[(Ephemeral OS /tmp)]

    Client -->|HTTPS / Next.js Routing| VercelEdge
    VercelEdge -->|Serves UI| Frontend
    Frontend -->|POST /api/process| Backend
    Backend -->|File I/O| Disk
    Backend -->|Model Operations| IfcLib
    IfcLib -->|Repaired Model| Disk
    Backend -->|GET /api/download| Client
```

---

## 2. Backend Module Dependencies

The backend is strictly modular. The main application router simply orchestrates distinct services for parsing, validating, repairing, and reporting.

```mermaid
graph TD
    Main[main.py - FastAPI Router]
    Parser[ifc_parser.py - Load/Save]
    Validator[validation.py - Detection]
    Repair[repair.py - Correction]
    Report[report.py - Data Formatting]
    Utils[utils.py - Logging & OS I/O]
    IfcOpenShell[IfcOpenShell Library]

    Main --> Parser
    Main --> Validator
    Main --> Repair
    Main --> Report
    Main --> Utils

    Parser --> IfcOpenShell
    Validator --> IfcOpenShell
    Repair --> IfcOpenShell
```

---

## 3. Data Flow Diagram

```mermaid
sequenceDiagram
    participant User as User Browser
    participant API as FastAPI Backend
    participant Disk as /tmp Storage
    participant Engine as IfcOpenShell Engine

    User->>API: Uploads model.ifc
    API->>Disk: Streams to secure temp file (UUID)
    API->>Engine: Loads IFC model into RAM
    Engine-->>API: Model loaded
    
    API->>Engine: Run Validation Rules
    Engine-->>API: Returns detected issues list
    
    API->>Engine: Run Repair Sequences
    Engine-->>API: Applies semantic fixes
    
    API->>Disk: Saves repaired_model.ifc
    API->>Disk: Deletes original input file securely
    
    API-->>User: Returns JSON Validation Report + Download URL
    
    User->>API: Clicks Download URL
    API->>Disk: Streams repaired_model.ifc
    API->>Disk: Deletes repaired_model.ifc via BackgroundTask
```

---

## 4. Database Architecture

Currently, the application runs entirely **Statelessly**. It operates as a strict utility API that adheres to strict zero-retention privacy policies. User files are deleted within seconds or minutes. 

### Future Database Architecture (Planned)
If user accounts, billing, and historic job tracking are implemented, a relational database (e.g., PostgreSQL) is recommended.

```mermaid
erDiagram
    USER ||--o{ JOB : runs
    JOB ||--|{ ISSUE : detects
    USER {
        uuid id PK
        string email
        string plan_type
    }
    JOB {
        uuid id PK
        uuid user_id FK
        datetime created_at
        int original_size_bytes
        int score
    }
    ISSUE {
        uuid id PK
        uuid job_id FK
        string issue_type
        int occurrences
        boolean repaired
    }
```

---

## 5. Deployment Architecture

### Scenario A: Vercel Only (Monorepo)
Both the Next.js frontend and the Python backend are hosted entirely within the Vercel ecosystem using Serverless Functions.

- **Frontend**: Standard Vercel Edge caching and static hosting.
- **Backend**: The `api/index.py` file serves as a wrapper to deploy the FastAPI application on AWS Lambda via Vercel's Serverless Python runtimes. Memory limits are constrained (up to 1024MB default), making it suitable for small-to-medium IFC files.

### Scenario B: Vercel + Google Cloud Run (Recommended for Heavy Processing)
To process massive IFC files (100MB+), the backend must be detached from serverless constraints and run inside a container.

- **Frontend**: Remains on Vercel.
- **Backend**: Containerized using the provided `Dockerfile` and deployed to Google Cloud Run, Railway, or AWS Fargate. 
- **Networking**: The Next.js frontend utilizes the `NEXT_PUBLIC_API_URL` environment variable to transparently direct uploads to the dedicated GPU/CPU Cloud Run container instead of the Vercel internal API.
