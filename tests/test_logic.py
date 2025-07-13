import unittest
from pricing_logic.material_db import get_material_info
from pricing_logic.labor_calc import get_labor_cost_and_time, get_task_zone
from utils.ai_transcript_parser import parse_transcript_ai

class TestPricingLogic(unittest.TestCase):

    def test_material_info(self):
        material, cost = get_material_info("install a vanity", 4)
        self.assertEqual(material, "vanity set")
        self.assertGreater(cost, 0)

    def test_labor_calc(self):
        hours, cost = get_labor_cost_and_time("repaint the walls", 1.0)
        self.assertAlmostEqual(hours, 1.5)
        self.assertGreater(cost, 0)

    def test_task_zone(self):
        zone = get_task_zone("replace the toilet")
        self.assertEqual(zone, "fixture install")

    def test_transcript_parser(self):
        transcript = "Paint the bathroom walls and install a vanity. Located in Marseille."
        result = parse_transcript_ai(transcript)
        self.assertEqual(result["city"], "marseille")
        self.assertGreaterEqual(len(result["tasks"]), 1)

if __name__ == "__main__":
    unittest.main()
