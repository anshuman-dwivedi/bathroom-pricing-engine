import json
from pricing_logic.material_db import get_material_info
from pricing_logic.labor_calc import get_labor_cost_and_time, get_task_zone
from pricing_logic.vat_rules import get_vat_rate
from utils.ai_transcript_parser import parse_transcript_ai as parse_transcript
# You can also use: from utils.transcript_parser import parse_transcript

# Supported cities and their labor cost multipliers
CITY_MULTIPLIERS = {
    "marseille": 1.0,
    "paris": 1.2
}

# Company margin setting
MARGIN = 0.15  # 15% profit

def generate_quote(transcript):
    parsed = parse_transcript(transcript)
    city = parsed.get("city", "marseille").lower()

    # Validate city
    if city not in CITY_MULTIPLIERS:
        print(f"⚠️ Warning: '{city}' is not in CITY_MULTIPLIERS. Using default multiplier 1.0")
        multiplier = 1.0
        quote_error_flags = [f"Unknown city '{city}' — default multiplier used."]
    else:
        multiplier = CITY_MULTIPLIERS[city]
        quote_error_flags = []

    size_m2 = parsed.get("size_m2", 4.0)

    # Base quote dictionary
    quote = {
        "location": city.capitalize(),
        "bathroom_size_m2": size_m2,
        "tasks": [],
        "confidence_score": parsed.get("confidence", 0.9),
        "error_flags": quote_error_flags
    }

    # 🚨 Error if no valid tasks found
    if not parsed["tasks"]:
        raise ValueError("❌ No valid renovation tasks were detected in the transcript.")

    # Loop through each parsed task
    for task in parsed["tasks"]:
        task_name = task["task"]
        zone = get_task_zone(task_name)

        # Skip if task is unknown
        if zone == "unknown":
            print(f"⚠️ Unknown task '{task_name}' not found in data files.")
            quote["error_flags"].append(f"Unknown task '{task_name}' — skipped.")
            continue

        material_name, material_cost = get_material_info(task_name, size_m2)
        labor_time, labor_cost = get_labor_cost_and_time(task_name, multiplier)

        subtotal = labor_cost + material_cost
        margin_amount = subtotal * MARGIN
        vat_rate = get_vat_rate(task_name, city)
        total_cost = (subtotal + margin_amount) * (1 + vat_rate)

        quote["tasks"].append({
            "zone": zone,
            "task": task_name,
            "material": material_name,
            "labor_hours": labor_time,
            "labor_cost": labor_cost,
            "material_cost": material_cost,
            "margin": MARGIN,
            "vat_rate": vat_rate,
            "total_cost": round(total_cost, 2)
        })

    # Grand total across all valid tasks
    quote["grand_total"] = round(sum(t["total_cost"] for t in quote["tasks"]), 2)
    return quote


# Main script entry
if __name__ == "__main__":
    transcript = (
         "Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, "
        "redo the for the shower. Budget-conscious. Located in Paris."
    )

    quote = generate_quote(transcript)

    with open("output/sample_quote.json", "w") as f:
        json.dump(quote, f, indent=2)

    print("✅ Quote generated and saved to output/sample_quote.json")
