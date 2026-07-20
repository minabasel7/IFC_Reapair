# IFC Repair & Validation SaaS

A production-ready SaaS application for validating and repairing OpenBIM IFC models. It detects semantic errors, duplicate GUIDs, missing relationships, and automatically repairs them without losing geometric data.

## Architecture

This project is built with a decoupled architecture:

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS, Framer Motion.
- **Backend**: FastAPI (Python 3.12), IfcOpenShell.

This structure allows you to deploy the application as a single monorepo on Vercel, or split them apart by deploying the frontend on Vercel and the backend on Google Cloud Run, Railway, or Render.

## Environment Variables

### Frontend (`.env.local`)
Create a `.env.local` file in the root directory:
```env
# URL for the Python Backend.
# If deploying both on Vercel, this is usually omitted as Vercel routes `/api` internally.
# If deploying backend to Cloud Run, set this to the Cloud Run URL (e.g. https://api.my-ifc-app.com/api)
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Running Locally

### 1. Start the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Start the Frontend
In a new terminal:
```bash
# Make sure you are in the root directory
npm install
npm run dev
```
Open `http://localhost:3000` to view the application.

## Deployment Instructions

### Option 1: Vercel (All-in-one)
The repository includes a `vercel.json` file configured to deploy both the Next.js frontend and the FastAPI backend together.
1. Push the code to a GitHub repository.
2. Import the project into Vercel.
3. Vercel will automatically detect Next.js and the `vercel.json` will configure the Python serverless functions.
> **Note**: Vercel has a 250MB limit for serverless functions on Hobby/Pro tiers. `IfcOpenShell` is large. If the deployment fails due to size limits, use Option 2.

### Option 2: Decoupled (Vercel Frontend + Cloud Run Backend)
If the backend exceeds Vercel limits, deploy it separately:
1. **Deploy Backend**: Use the provided `backend/Dockerfile` to deploy the Python app to Google Cloud Run, Render, or Railway.
2. **Deploy Frontend**: Deploy the root directory to Vercel.
3. **Configure**: Set the `NEXT_PUBLIC_API_URL` environment variable in Vercel to point to your new backend URL.

## Privacy & Security
- **No Database**: Uploaded models are never stored permanently.
- **Ephemeral Storage**: Files are processed in `/tmp` and securely deleted immediately after processing.

## Future Roadmap
- Integration with Stripe for Pay-per-file or subscriptions.
- Batch processing support.
- User accounts and dashboard history.
- AI-assisted repair suggestions.
