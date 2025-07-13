# Import the regular expression library to help extract patterns from text
import re

def parse_transcript(transcript):

    # Convert the entire transcript to lowercase to make matching easier

    transcript = transcript.lower()

    # Detect city
    city_match = re.search(r"located in (\w+)", transcript)
    city = city_match.group(1) if city_match else "marseille"

    # Detect bathroom size
    size_match = re.search(r"(\d+(\.\d+)?)\s?m[\u00b2^2]", transcript)
    size_m2 = float(size_match.group(1)) if size_match else 4.0

    # Extract tasks (basic matching)
    tasks_list = []
    tasks = {
        "remove old tiles": "floor demolition",
        "redo the plumbing": "plumbing",
        "replace the toilet": "fixture install",
        "install a vanity": "fixture install",
        "repaint the walls": "painting",
        "lay new ceramic floor tiles": "floor install"
    }
 # If a task phrase is found in the transcript, add it to the task list
    for key, zone in tasks.items():
        if key in transcript:
            tasks_list.append({"task": key, "zone": zone})
 #If 4 or more known tasks are found, confidence is high (0.9), else lower (0.6)
    confidence = 0.9 if len(tasks_list) >= 4 else 0.6

 # Return all extracted information as a dictionary
    return {
        "city": city,
        "size_m2": size_m2,
        "tasks": tasks_list,
        "confidence": confidence
    }
