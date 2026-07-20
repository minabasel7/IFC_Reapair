import os
import sys
import shutil

# Tell Vercel's Python runtime to look for modules inside the 'api' folder
sys.path.append(os.path.dirname(__file__))
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import our processing modules
from ifc_parser import IFCParser
from validation import IFCValidator
from repair import IFCRepair
from report import ReportGenerator
from utils import get_temp_file_path, secure_delete_file, logger

app = Flask(__name__)
# Enable CORS for the frontend if hosted on a different domain, otherwise optional
CORS(app)

@app.route('/api/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    temp_input_path = get_temp_file_path(extension=".ifc")
    temp_output_path = get_temp_file_path(extension="_repaired.ifc")
    
    try:
        # Save the uploaded file to a temporary location
        file.save(temp_input_path)
        
        # 1. Parse
        parser = IFCParser(temp_input_path)
        model = parser.load_model()
        stats = parser.get_basic_stats()
        
        # 2. Validate
        validator = IFCValidator(model)
        issues = validator.validate()
        
        # 3. Repair
        repair_engine = IFCRepair(model, issues)
        repairs_made = repair_engine.repair()
        
        # Save repaired model
        parser.save_model(temp_output_path)
        
        # 4. Generate Report
        report_generator = ReportGenerator(stats, issues, repairs_made)
        report = report_generator.generate_summary()
        
        # Read the repaired file back into memory to send it to the client
        with open(temp_output_path, "rb") as f:
            file_data = f.read()
            
        import base64
        file_base64 = base64.b64encode(file_data).decode('utf-8')
            
        # We return the report and the file in a single JSON response
        return jsonify({
            "report": report,
            "repaired_file_base64": file_base64
        })

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
    finally:
        # Clean up temp files
        secure_delete_file(temp_input_path)
        secure_delete_file(temp_output_path)

# Vercel serverless function entrypoint requires the 'app' variable to be exposed
