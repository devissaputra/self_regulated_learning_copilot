import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from self_regulated_learning_copilot import core


class CoreTests(unittest.TestCase):
    def test_support_policy(self):
        state = core.SRLState(0.2, 0.2, 0.7, 18)
        self.assertEqual(core.support_level(state), "guided_hint")
        self.assertIn("smallest part", core.reflection_prompt(state))

    def test_state_validation(self):
        with self.assertRaises(ValueError):
            core.SRLState(1.2, 0.5, 0.5, 0)


if __name__ == "__main__":
    unittest.main()
