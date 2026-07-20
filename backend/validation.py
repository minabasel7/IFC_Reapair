import ifcopenshell
from utils import logger

class IFCValidator:
    def __init__(self, model: ifcopenshell.file):
        self.model = model
        self.issues = []
        self.score = 100

    def validate(self) -> dict:
        """
        Runs a suite of validation checks on the loaded IFC model.
        Returns a dictionary of found issues and a validation score.
        """
        logger.info("Starting IFC validation...")
        self._check_duplicate_guids()
        self._check_spatial_hierarchy()
        self._check_empty_property_sets()
        self._check_missing_placements()

        # Calculate a rough score based on the number of issues
        penalty = len(self.issues) * 5
        self.score = max(0, 100 - penalty)

        return {
            "score": self.score,
            "issues": self.issues,
            "total_issues": len(self.issues)
        }

    def _check_duplicate_guids(self):
        """Finds elements with duplicate GlobalIds."""
        guids = set()
        for element in self.model.by_type("IfcRoot"):
            if element.GlobalId in guids:
                self.issues.append({
                    "type": "duplicate_guid",
                    "severity": "high",
                    "entity_id": element.id(),
                    "entity_type": element.is_a(),
                    "message": f"Duplicate GlobalId found: {element.GlobalId}"
                })
            else:
                guids.add(element.GlobalId)

    def _check_spatial_hierarchy(self):
        """Finds building elements that are not assigned to a spatial structure."""
        building_elements = self.model.by_type("IfcBuildingElement")
        
        for element in building_elements:
            # Check IfcRelContainedInSpatialStructure
            contained = False
            # Fix: safely handle cases where ContainedInStructure exists but is None
            inverse_rels = getattr(element, "ContainedInStructure", None) or []
            for rel in inverse_rels:
                if rel.is_a("IfcRelContainedInSpatialStructure"):
                    contained = True
                    break
            
            if not contained:
                self.issues.append({
                    "type": "missing_spatial_hierarchy",
                    "severity": "medium",
                    "entity_id": element.id(),
                    "entity_type": element.is_a(),
                    "message": f"Element is not contained in any spatial structure."
                })

    def _check_empty_property_sets(self):
        """Finds property sets that have no properties attached."""
        psets = self.model.by_type("IfcPropertySet")
        for pset in psets:
            if not pset.HasProperties:
                self.issues.append({
                    "type": "empty_property_set",
                    "severity": "low",
                    "entity_id": pset.id(),
                    "entity_type": "IfcPropertySet",
                    "message": f"Property set '{pset.Name}' contains no properties."
                })

    def _check_missing_placements(self):
        """Finds products that require a placement but don't have one."""
        products = self.model.by_type("IfcProduct")
        for product in products:
            if not product.ObjectPlacement:
                self.issues.append({
                    "type": "missing_placement",
                    "severity": "high",
                    "entity_id": product.id(),
                    "entity_type": product.is_a(),
                    "message": "Product is missing an ObjectPlacement."
                })
