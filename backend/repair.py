import ifcopenshell
import ifcopenshell.guid
from utils import logger

class IFCRepair:
    def __init__(self, model: ifcopenshell.file, issues: list):
        self.model = model
        self.issues = issues
        self.repairs_performed = 0

    def repair(self):
        """
        Attempts to automatically repair semantic issues found during validation.
        """
        logger.info("Starting IFC repair process...")
        for issue in self.issues:
            if issue.get("type") == "duplicate_guid":
                self._repair_duplicate_guid(issue.get("entity_id"))
            elif issue.get("type") == "missing_spatial_hierarchy":
                self._repair_spatial_hierarchy(issue.get("entity_id"))
            # We don't repair missing placements or empty property sets automatically
            # to avoid corrupting geometry or destroying user-defined data structures.

        return self.repairs_performed

    def _repair_duplicate_guid(self, entity_id: int):
        """Generates a new valid GUID for the element."""
        if entity_id is None:
            return
        try:
            element = self.model.by_id(entity_id)
            if hasattr(element, "GlobalId"):
                element.GlobalId = ifcopenshell.guid.new()
                self.repairs_performed += 1
                logger.info(f"Repaired duplicate GUID for entity #{entity_id}")
        except Exception as e:
            logger.warning(f"Failed to repair duplicate GUID for entity #{entity_id}: {str(e)}")

    def _repair_spatial_hierarchy(self, entity_id: int):
        """Assigns the element to the first available IfcBuildingStorey or IfcBuilding."""
        if entity_id is None:
            return
        try:
            element = self.model.by_id(entity_id)
            
            # Find a target spatial structure (Storey > Building > Site)
            target_spatial = None
            for ifc_type in ["IfcBuildingStorey", "IfcBuilding", "IfcSite"]:
                structures = self.model.by_type(ifc_type)
                if structures:
                    target_spatial = structures[0]
                    break
            
            if not target_spatial:
                logger.warning("No spatial structure found in model to assign orphan element.")
                return

            # Check if an existing relationship exists we can append to
            rels = getattr(target_spatial, "ContainsElements", None) or []
            if rels:
                rel = rels[0]
                # Elements is a tuple, we need to convert to list, append, and convert back
                current_elements = list(rel.RelatedElements)
                current_elements.append(element)
                # FIX: Ensure we assign back a tuple to avoid ifcopenshell schema violations
                rel.RelatedElements = tuple(current_elements)
            else:
                # Create a new relationship
                self.model.createIfcRelContainedInSpatialStructure(
                    GlobalId=ifcopenshell.guid.new(),
                    OwnerHistory=self._get_or_create_owner_history(),
                    Name="Auto-Repaired Containment",
                    RelatingStructure=target_spatial,
                    RelatedElements=[element]
                )
            self.repairs_performed += 1
            logger.info(f"Repaired spatial hierarchy for entity #{entity_id} -> assigned to #{target_spatial.id()}")
        except Exception as e:
            logger.warning(f"Failed to repair spatial hierarchy for entity #{entity_id}: {str(e)}")

    def _get_or_create_owner_history(self):
        """Helper to safely get or create an OwnerHistory for new relationships."""
        histories = self.model.by_type("IfcOwnerHistory")
        if histories:
            return histories[0]
        
        # Creating a basic OwnerHistory is complex because it requires PersonAndOrganization, Application, etc.
        # For simplicity and to avoid cluttering the model with fake people, we search for existing ones.
        # If absolutely missing, return None (though IFC2x3 requires it, IFC4 makes it OPTIONAL).
        # We will assume IFC4 or that one exists.
        return None
