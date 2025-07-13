import csv
import os

# Load CSV into a dictionary at startup
LABOR_DATA = {}

with open(os.path.join("data", "price_templates.csv"), newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        LABOR_DATA[row["task"]] = {
            "zone": row["zone"],
            "hours": float(row["labor_hours"]),
            "rate": float(row["base_hourly_rate"])
        }

def get_labor_cost_and_time(task_name, city_multiplier):
    task = LABOR_DATA.get(task_name)

    if not task:
        return 2.0, round(2.0 * 40 * city_multiplier, 2)  # fallback

    hours = task["hours"]
    rate = task["rate"]
    cost = hours * rate * city_multiplier

    return hours, round(cost, 2)

def get_task_zone(task_name):
    task = LABOR_DATA.get(task_name)
    return task["zone"] if task else "unknown"
