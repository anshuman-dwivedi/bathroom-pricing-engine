import re

def parse_transcript_fallback(transcript):
    transcript_clean = re.sub(r"[^\w\s]", "", transcript.lower())  # remove punctuation
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

    # Extract city-like words using regex
    original_city = None
    city_match = re.search(r"located in ([a-zA-Z\s]+)", transcript.lower())
    if city_match:
        original_city = city_match.group(1).strip()
    else:
        original_city = "unknown"

    supported_cities = list(CITY_MULTIPLIERS.keys())
    detected_city = None
    for city in supported_cities:
        if city in transcript.lower():
            detected_city = city
            break

    city_warning = False
    if not detected_city:
        detected_city = "marseille"
        city_warning = True

    return {
        "city": detected_city,
        "original_city": original_city,
        "size_m2": 4.0,
        "confidence": 0.6,
        "tasks": tasks_found,
        "city_warning": city_warning
    }
