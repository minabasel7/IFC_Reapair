import os
import uuid
import tempfile
import logging

# Configure basic logging, ensuring we never log IFC contents or building info
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("IFC-SaaS")

def get_temp_file_path(extension=".ifc") -> str:
    """
    Returns a secure temporary file path that will be used for processing.
    The file will be stored in the OS temp directory and given a random UUID.
    """
    tmp_dir = tempfile.gettempdir()
    file_name = f"{uuid.uuid4()}{extension}"
    return os.path.join(tmp_dir, file_name)

def secure_delete_file(file_path: str):
    """
    Securely deletes a temporary file to comply with privacy requirements.
    Never store user files permanently.
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Securely deleted temporary file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete temporary file {file_path}: {str(e)}")
