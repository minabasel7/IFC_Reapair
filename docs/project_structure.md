# Project Structure & Environment Variables

## Folder Structure

The repository is organized into distinct domains for the frontend and backend to allow for easy separation if microservices deployment is needed in the future.

```text
ifc-repair-saas/
├── app/                  # Next.js App Router (Frontend Pages)
│   ├── dashboard/        # The main upload and reporting interface
│   ├── globals.css       # Global Tailwind CSS definitions
│   ├── layout.tsx        # Root layout, HTML wrappers, fonts
│   └── page.tsx          # Landing page
├── components/           # Reusable React UI Components
│   └── file-uploader.tsx # Complex drag-and-drop file upload logic
├── backend/              # Python Processing Engine
│   ├── main.py           # FastAPI entrypoint and HTTP routing
│   ├── ifc_parser.py     # Wrappers for IfcOpenShell I/O
│   ├── validation.py     # Rule engine for detecting IFC defects
│   ├── repair.py         # Automated semantic resolution strategies
│   ├── report.py         # Formats validation metrics into JSON
│   ├── utils.py          # Secure OS file handling & logging
│   └── requirements.txt  # Python package dependencies
├── docs/                 # Project documentation
├── public/               # Static frontend assets (images, fonts)
├── vercel.json           # Vercel deployment routing configuration
├── tailwind.config.ts    # Frontend design system token configuration
└── next.config.mjs       # Next.js build configuration
```

## Environment Variables

Communication between the Next.js frontend and the FastAPI backend is managed via environment variables. This allows the backend to be detached from Vercel without altering the source code.

### Frontend Variables

- **`NEXT_PUBLIC_API_URL`**
  - **Description**: Defines the base URL where the frontend will send `POST /process` requests.
  - **Default**: `/api` (Assumes the backend is running on the same domain, configured via Vercel Rewrites).
  - **Example for Remote Backend**: `https://my-ifc-engine.a.run.app/api`

### Backend Variables

- *(No mandatory environment variables required for core processing)*. 
- The backend relies securely on standard Python OS modules for generating `/tmp` directories dynamically depending on the host OS or container environment.
