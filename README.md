# 🛁 Bathroom Smart Pricing Engine

A Python-based pricing engine that reads a natural language transcript (e.g., a bathroom renovation request) and generates a structured, task-based renovation quote in JSON format.

---

# Features

- Parses unstructured natural language transcripts
- Detects key renovation components: toilet, shower, vanity, etc.
- Applies predefined pricing for each component
- Adjusts pricing based on city using a city multiplier
- Outputs a detailed breakdown and total estimated cost

---

##  Example Transcript

Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, redo the plumbing for the shower, replace the toilet, install a vanity, repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille.


--- 

## How to Run Code

Install Python and required packages, then run the script using:

python pricing_engine.py

The output will be saved to output/sample_quote.json.

---

## Explanation Of Pricing Logic

The pricing logic extracts renovation items (like sink, tiles, shower) from customer inputs using basic NLP or keyword matching. Each item is mapped to a predefined price list, and total cost is calculated based on quantity, area, and quality. Labor, service, and tax are added to generate the final estimate. The system supports transcript or form-based inputs and returns a detailed cost breakdown.

## ✅ Output Example (sample_quote.json) / Schema of output JSON

```json
{
  "location": "Marseille",
  "bathroom_size_m2": 4,
  "tasks": [
    {
      "zone": "fixture install",
      "task": "install a vanity",
      "material": "N/A",
      "labor_hours": 2.0,
      "labor_cost": 80.0,
      "material_cost": 250.0,
      "margin": 0.15,
      "vat_rate": 0.2,
      "total_cost": 455.4
    }
  ],
  "grand_total": 1424.16,
  "confidence_score": 0.92,
  "error_flags": []
}

--

## Project Structure

bathroom-pricing-engine/
├── pricing_engine.py              # Main script
├── pricing_logic/                # Logic modules
│   ├── material_db.py            # Material cost mapping
│   ├── labor_calc.py             # Labor time & pricing
│   └── vat_rules.py              # VAT rules per task
├── utils/                        # Parsing transcript
│   └── transcript_parser.py
|   └── ai_transcript_parser.py
├── output/                       # Where quote JSON is saved
│   └── sample_quote.json
├── tests/                        # Unit tests
│   └── test_logic.py
├── README.md

---

## Any assumptions or edge cases handled:

1. Supported Cities / Regions
The pricing engine currently supports two French cities:

Marseille

Paris

These were chosen based on the sample transcript provided in the prompt, which mentioned Marseille, and an additional common city (Paris) to simulate regional variation.

2.City-Based Labor Cost Multiplier
Labor cost differs by city, simulating real-world economic conditions.

A multiplier is applied to the base hourly labor rate:

City	Multiplier	Assumption
Marseille	1.0	 Baseline labor cost reference
Paris	    1.2	 Labor in Paris is 20% more expensive due to higher cost of living

Cities not listed in the system will:

⚠️ Trigger a warning

Default to multiplier = 1.0

Log an error flag in the final quote

3. Handling Unknown or Unsupported Regions
If the transcript includes a city not listed in CITY_MULTIPLIERS, the system:

Prints a warning message in the console

Adds an error_flag in the final JSON quote

Continues with default pricing logic using multiplier = 1.0

---

Author
Anshuman Dwivedi  
LinkedIn (https://www.linkedin.com/in/anshuman-dwivedi-)
