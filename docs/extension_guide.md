# Future Extension Guide

The IFC Repair SaaS backend is designed to be highly modular. New validation rules and repair strategies can be added without modifying the core API routing or parsing engine.

## 1. Adding a New Validation Rule

All semantic validations occur within `backend/validation.py` inside the `IFCValidator` class. 

### Step-by-step
1. **Create the Rule Method**: Define a new private method prefixed with `_check_` (e.g., `_check_missing_materials(self)`).
2. **Execute the Query**: Use `self.model.by_type(...)` to query the relevant entities.
3. **Register the Issue**: If a defect is found, append a dictionary to `self.issues`. The dictionary **must** contain `type`, `severity`, `entity_id`, and `message`.
4. **Invoke the Rule**: Add your new method to the sequence inside the `validate(self)` master method.

**Example Implementation:**
```python
def _check_missing_materials(self):
    """Finds physical elements missing material assignments."""
    elements = self.model.by_type("IfcBuildingElement")
    for element in elements:
        has_material = getattr(element, "HasAssociations", None)
        # Simplified check
        if not has_material:
            self.issues.append({
                "type": "missing_material",
                "severity": "low",
                "entity_id": element.id(),
                "entity_type": element.is_a(),
                "message": f"Element {element.GlobalId} has no assigned material."
            })
```

## 2. Adding a New Repair Strategy

All automated repairs occur within `backend/repair.py` inside the `IFCRepair` class. 

### Step-by-step
1. **Create the Repair Method**: Define a new private method prefixed with `_repair_` (e.g., `_repair_missing_material(self, entity_id: int)`).
2. **Handle the Entity**: Look up the entity via `self.model.by_id(entity_id)`.
3. **Apply the Fix**: Create new entities or modify attributes. Ensure you cast any modified `ifcopenshell` list properties back to tuples.
4. **Log & Increment**: Increment `self.repairs_performed` and log the fix.
5. **Route the Issue Type**: Add an `elif` block in the `repair(self)` master method matching the `type` string defined in your validation rule.

**Example Implementation:**
```python
# Inside the repair(self) loop:
# elif issue.get("type") == "missing_material":
#     self._repair_missing_material(issue.get("entity_id"))

def _repair_missing_material(self, entity_id: int):
    """Assigns a default generic material to the element."""
    if entity_id is None: return
    try:
        element = self.model.by_id(entity_id)
        
        # 1. Check if a default material exists, else create it
        materials = self.model.by_type("IfcMaterial")
        default_mat = next((m for m in materials if m.Name == "Generic Auto-Repair"), None)
        if not default_mat:
            default_mat = self.model.createIfcMaterial(Name="Generic Auto-Repair")
            
        # 2. Assign material
        self.model.createIfcRelAssociatesMaterial(
            GlobalId=ifcopenshell.guid.new(),
            OwnerHistory=self._get_or_create_owner_history(),
            Name="Auto Material Assignment",
            RelatedObjects=[element],
            RelatingMaterial=default_mat
        )
        
        self.repairs_performed += 1
        logger.info(f"Repaired missing material for entity #{entity_id}")
    except Exception as e:
        logger.warning(f"Failed to repair material for entity #{entity_id}: {str(e)}")
```

## Best Practices
- **Do no harm**: If a repair requires destructive changes to geometry, do not execute it automatically.
- **Fail Gracefully**: Always wrap repair strategies in `try...except` blocks to ensure one failing repair does not halt the entire process.
- **Tuples for Inverse Relationships**: When modifying existing IFC relationships in `ifcopenshell`, always cast Python lists back to `tuple` before assignment (e.g., `rel.RelatedElements = tuple(my_list)`).
