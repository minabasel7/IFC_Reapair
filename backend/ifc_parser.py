import ifcopenshell
from utils import logger

class IFCParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.model = None

    def load_model(self) -> ifcopenshell.file:
        """
        Safely loads the IFC model into memory.
        Raises an exception if the file is invalid or corrupted.
        """
        logger.info(f"Loading IFC model from temporary storage.")
        try:
            self.model = ifcopenshell.open(self.file_path)
            return self.model
        except Exception as e:
            logger.error(f"Failed to load IFC model: {str(e)}")
            raise ValueError("Invalid or corrupted IFC file. Could not parse.")

    def get_basic_stats(self) -> dict:
        """
        Returns high-level statistics about the loaded model.
        """
        if not self.model:
            raise ValueError("Model not loaded.")

        schema = self.model.schema
        entities_count = len(self.model.by_type("IfcRoot"))
        
        return {
            "schema": schema,
            "entities_count": entities_count
        }

    def save_model(self, output_path: str):
        """
        Saves the current state of the model to a file.
        """
        if not self.model:
            raise ValueError("Model not loaded.")
        
        logger.info(f"Saving repaired IFC model to {output_path}")
        self.model.write(output_path)
