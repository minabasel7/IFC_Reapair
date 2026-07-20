import os
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import threading

from ifc_parser import IFCParser
from validation import IFCValidator
from repair import IFCRepair
from report import ReportGenerator
from utils import get_temp_file_path, secure_delete_file, logger

app = FastAPI(title="IFC Repair SaaS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "IFC Repair Engine"}

@app.post("/api/process")
async def process_ifc(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".ifc"):
        raise HTTPException(status_code=400, detail="Only .ifc files are supported")

    temp_input_path = get_temp_file_path()
    temp_output_path = get_temp_file_path(extension="_repaired.ifc")

    try:
        with open(temp_input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Received file: {file.filename}")

        parser = IFCParser(temp_input_path)
        model = parser.load_model()
        stats = parser.get_basic_stats()

        val_start = time.time()
        validator = IFCValidator(model)
        validation_results = validator.validate()
        val_end = time.time()

        rep_start = time.time()
        repair_engine = IFCRepair(model, validation_results["issues"])
        repairs_performed = repair_engine.repair()
        parser.save_model(temp_output_path)
        rep_end = time.time()

        val_time_ms = round((val_end - val_start) * 1000, 2)
        rep_time_ms = round((rep_end - rep_start) * 1000, 2)

        file_id = os.path.basename(temp_output_path)
        report_generator = ReportGenerator(stats, validation_results, repairs_performed, val_time_ms, rep_time_ms)
        report_data = report_generator.generate_json(download_url=f"/api/download/{file_id}")
        
        secure_delete_file(temp_input_path)
        
        # Schedule a cleanup of the output file after 10 minutes in case it is never downloaded
        timer = threading.Timer(600.0, secure_delete_file, args=[temp_output_path])
        timer.daemon = True
        timer.start()

        return JSONResponse(content=report_data)

    except Exception as e:
        secure_delete_file(temp_input_path)
        secure_delete_file(temp_output_path)
        logger.error(f"Processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{file_id}")
async def download_file(file_id: str):
    import tempfile
    from fastapi.background import BackgroundTasks
    
    # SECURITY: Prevent path traversal by extracting only the basename
    safe_file_id = os.path.basename(file_id)
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, safe_file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found or already deleted.")

    def cleanup():
        secure_delete_file(file_path)

    background_tasks = BackgroundTasks()
    background_tasks.add_task(cleanup)

    return FileResponse(
        path=file_path, 
        filename="repaired_model.ifc", 
        media_type="application/octet-stream",
        background=background_tasks
    )
