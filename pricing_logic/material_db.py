import json
import os

# Load the materials.json once
with open(os.path.join("data", "materials.json")) as f:
    MATERIALS = json.load(f)

def get_material_info(task_name, size_m2):
    task_data = MATERIALS.get(task_name)

    if not task_data:
        return "unknown", 0

    material_name = task_data.get("material", "unknown")
    unit_cost = task_data.get("unit_cost", 0)

    if task_data.get("unit") == "m2":
        if "wall_height_m" in task_data:
            cost = unit_cost * size_m2 * task_data["wall_height_m"]  # for walls
        else:
            cost = unit_cost * size_m2  # for floor
    else:
        cost = unit_cost  # fixed cost

    return material_name, round(cost, 2)

