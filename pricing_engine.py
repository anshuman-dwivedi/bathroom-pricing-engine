import json
import re
from pricing_logic.material_db import get_material_info
from pricing_logic.labor_calc import get_labor_cost_and_time, get_task_zone
from pricing_logic.vat_rules import get_vat_rate

# Try to import AI parser
from utils.ai_transcript_parser import parse_transcript_ai as parse_transcript

# Supported cities and their labor multipliers
CITY_MULTIPLIERS = {
    "marseille": 1.0,
    "paris": 1.2
}

MARGIN = 0.15  # 15% company margin


# -----------------------------
# Fallback Transcript Parser
# -----------------------------
def parse_transcript_fallback(transcript):
    transcript_clean = re.sub(r"[^\w\s]", "", transcript.lower())
    tasks_found = []

    VARIANT_TASK_MAP = {
        "remove the old tiles": "remove old tiles",
        "remove old tiles": "remove old tiles",
        "redo the plumbing for the shower": "redo the plumbing",
        "redo the plumbing": "redo the plumbing",
        "replace the toilet": "replace the toilet",
        "install a vanity": "install a vanity",
        "repaint the walls": "repaint the walls",
        "paint the walls": "repaint the walls",
        "lay new ceramic floor tiles": "lay new ceramic floor tiles",
        "install ceramic floor tiles": "lay new ceramic floor tiles"
    }

    matched_standard_tasks = set()
    for variant, standard in VARIANT_TASK_MAP.items():
        pattern = variant.replace(" ", r"\s+")
        if re.search(pattern, transcript_clean):
            matched_standard_tasks.add(standard)

    tasks_found = [{"task": task} for task in matched_standard_tasks]

    # Try to extract original city from "located in <city>"
    city_match = re.search(r"located in ([a-z\s]+)", transcript.lower())
    original_city = city_match.group(1).strip() if city_match else "unknown"

    supported_cities = list(CITY_MULTIPLIERS.keys())
    detected_city = None
    for city in supported_cities:
        if city in transcript.lower():
            detected_city = city
            break

    city_warning = False
    if not detected_city:
        detected_city = "marseille"  # fallback city
        city_warning = True

    return {
        "city": detected_city,
        "original_city": original_city,
        "size_m2": 4.0,
        "confidence": 0.6,
        "tasks": tasks_found,
        "city_warning": city_warning
    }


# -----------------------------
# Quote Generator
# -----------------------------
def generate_quote(transcript):
    try:
        parsed = parse_transcript(transcript)
        if len(parsed.get("tasks", [])) < 6:
            print("⚠️ AI parser missed tasks, switching to fallback...")
            parsed = parse_transcript_fallback(transcript)
    except Exception as e:
        print(f"❌ AI parser failed: {e}. Switching to fallback...")
        parsed = parse_transcript_fallback(transcript)

    city = parsed.get("city", "marseille").lower()
    original_city = parsed.get("original_city", city)
    quote_error_flags = []

    if parsed.get("city_warning") or city not in CITY_MULTIPLIERS:
        print(f"⚠️ Warning: '{original_city}' is not in CITY_MULTIPLIERS. Using default multiplier 1.0")
        quote_error_flags.append(f"Unknown city '{original_city}' — default multiplier used.")
        multiplier = 1.0
    else:
        multiplier = CITY_MULTIPLIERS[city]

    size_m2 = parsed.get("size_m2", 4.0)

    quote = {
        "location": city.capitalize(),
        "bathroom_size_m2": size_m2,
        "tasks": [],
        "confidence_score": parsed.get("confidence", 0.9),
        "error_flags": quote_error_flags
    }

    if not parsed["tasks"]:
        raise ValueError("❌ No renovation tasks detected.")

    print("🔍 Parsed tasks:")
    for t in parsed["tasks"]:
        print("-", t["task"])

    # Optional task normalization
    NORMALIZED_TASK_MAP = {
        "remove the old tiles": "remove old tiles",
        "redo the plumbing for the shower": "redo the plumbing"
    }

    for task in parsed["tasks"]:
        original_task_name = task["task"].strip().lower()
        task_name = NORMALIZED_TASK_MAP.get(original_task_name, original_task_name)

        zone = get_task_zone(task_name)
        if zone == "unknown":
            print(f"⚠️ Skipping unknown task: {task_name}")
            quote["error_flags"].append(f"Unknown task '{original_task_name}' — skipped.")
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

    quote["grand_total"] = round(sum(t["total_cost"] for t in quote["tasks"]), 2)
    return quote


# -----------------------------
# Script Runner
# -----------------------------
if __name__ == "__main__":
    transcript = (
        "Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, "
        "redo the plumbing for the shower, replace the toilet, install a vanity, "
        "repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Pakistan."
    )

    quote = generate_quote(transcript)

    with open("output/sample_quote.json", "w") as f:
        json.dump(quote, f, indent=2)

    print("✅ Quote saved to output/sample_quote.json")
