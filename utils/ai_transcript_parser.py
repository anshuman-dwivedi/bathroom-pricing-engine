from sentence_transformers import SentenceTransformer, util
import re

# Load a small embedding model from Hugging Face (free, local)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define known task types and zones
KNOWN_TASKS = {
    "remove old tiles": "floor demolition",
    "redo the plumbing": "plumbing",
    "replace the toilet": "fixture install",
    "install a vanity": "fixture install",
    "repaint the walls": "painting",
    "lay ceramic floor tiles": "floor install"
}

def parse_transcript_ai(transcript):
    transcript = transcript.lower()

    # --- Extract city ---
    city_match = re.search(r"located in (\w+)", transcript)
    city = city_match.group(1) if city_match else "marseille"

    # --- Extract size ---
    size_match = re.search(r"(\d+(\.\d+)?)\s?m[²^2]", transcript)
    size_m2 = float(size_match.group(1)) if size_match else 4.0

    # --- AI-based fuzzy task detection ---
    found_tasks = []
    transcript_sentences = [s.strip() for s in re.split(r"[.]", transcript) if s]

    for sentence in transcript_sentences:
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)

        for known_task, zone in KNOWN_TASKS.items():
            task_embedding = model.encode(known_task, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(sentence_embedding, task_embedding).item()
           #for debugging
           # print(f"Checking: '{sentence}' vs '{known_task}' → Similarity: {similarity:.2f}")

            if similarity > 0.45:  # Adjust threshold as needed
                found_tasks.append({"task": known_task, "zone": zone})
    
    # Basic confidence logic
    confidence = 0.9 if len(found_tasks) >= 4 else 0.6

    return {
        "city": city,
        "size_m2": size_m2,
        "tasks": found_tasks,
        "confidence": confidence
    }
