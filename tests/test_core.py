import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from self_regulated_learning_copilot import core


def state(**overrides):
    base = {
        "mastery": 0.5,
        "confidence": 0.5,
        "effort": 0.6,
        "stalled_minutes": 2,
        "goal": "Complete the analysis",
        "goal_progress": 0.4,
        "next_action": "Fit a baseline",
        "success_evidence": "Baseline metric recorded",
        "current_strategy": "worked example",
        "strategy_effectiveness": 0.6,
        "recent_progress": 0.4,
        "monitoring_accuracy": 0.7,
        "learner_requested_help": False,
        "support_preference": "normal",
        "minutes_since_support": 999,
        "support_count": 0,
        "reflection_due": False,
        "task_difficulty": 0.5,
        "time_pressure": 0.5,
    }
    base.update(overrides)
    return core.SRLState(**base)


class CoreTests(unittest.TestCase):
    def test_original_positional_state_still_works(self):
        value = core.SRLState(0.2, 0.2, 0.7, 18)
        self.assertEqual(value.mastery, 0.2)

    def test_state_rejects_out_of_range_value(self):
        with self.assertRaises(ValueError):
            state(mastery=1.2)

    def test_state_rejects_boolean_numeric(self):
        with self.assertRaises(ValueError):
            state(effort=True)

    def test_state_rejects_nan_stall(self):
        with self.assertRaises(ValueError):
            state(stalled_minutes=math.nan)

    def test_state_rejects_infinite_minutes_since_support(self):
        with self.assertRaises(ValueError):
            state(minutes_since_support=math.inf)

    def test_state_rejects_bad_support_preference(self):
        with self.assertRaises(ValueError):
            state(support_preference="always")

    def test_policy_config_validation(self):
        with self.assertRaises(ValueError):
            core.PolicyConfig(
                mild_stall_minutes=20,
                hint_stall_minutes=10,
            )

    def test_plan_completeness_full(self):
        self.assertEqual(core.plan_completeness(state()), 1.0)

    def test_plan_completeness_partial(self):
        value = state(
            next_action=None,
            success_evidence=None,
        )
        self.assertEqual(core.plan_completeness(value), 0.5)

    def test_no_plan_prompts_planning(self):
        value = state(
            goal=None,
            next_action=None,
            success_evidence=None,
            current_strategy=None,
            recent_progress=0.1,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "planning_prompt")

    def test_silent_monitor_is_really_silent(self):
        value = state()
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "silent_monitor")
        self.assertFalse(decision["interrupt"])
        self.assertIsNone(core.render_support(decision, value))

    def test_opt_out_is_respected(self):
        value = state(support_preference="off")
        decision = core.decide_support(value)
        self.assertEqual(decision["reason"], "learner_opted_out")
        self.assertFalse(decision["interrupt"])

    def test_help_request_can_override_opt_out(self):
        value = state(
            support_preference="off",
            learner_requested_help=True,
            stalled_minutes=20,
            recent_progress=0.0,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "guided_hint")

    def test_cooldown_prevents_repeat_prompt(self):
        value = state(
            minutes_since_support=5,
            recent_progress=0.0,
            strategy_effectiveness=0.1,
            stalled_minutes=20,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["reason"], "support_cooldown")

    def test_prompt_burden_limit(self):
        value = state(
            support_count=4,
            recent_progress=0.0,
            strategy_effectiveness=0.1,
            stalled_minutes=20,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["reason"], "prompt_burden_limit")

    def test_reflection_prompt_on_completed_goal(self):
        value = state(goal_progress=0.96)
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "reflection_prompt")

    def test_reflection_due_triggers_reflection(self):
        value = state(reflection_due=True)
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "reflection_prompt")

    def test_help_request_during_stall_gets_hint(self):
        value = state(
            learner_requested_help=True,
            stalled_minutes=18,
            recent_progress=0.1,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "guided_hint")
        self.assertIn("show_hint", decision["choices"])

    def test_help_request_without_stall_gets_choice(self):
        value = state(learner_requested_help=True)
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "choice_prompt")

    def test_productive_struggle_is_not_interrupted(self):
        value = state(
            stalled_minutes=12,
            effort=0.9,
            recent_progress=0.4,
            strategy_effectiveness=0.8,
        )
        self.assertEqual(
            core.classify_struggle(value),
            "productive",
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "silent_monitor")
        self.assertEqual(decision["reason"], "productive_struggle")

    def test_productive_struggle_overrides_incomplete_plan_prompt(self):
        value = state(
            stalled_minutes=12,
            effort=0.9,
            recent_progress=0.4,
            strategy_effectiveness=0.8,
            next_action=None,
            success_evidence=None,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "silent_monitor")
        self.assertEqual(decision["reason"], "productive_struggle")

    def test_unproductive_struggle_offers_choice_before_hint(self):
        value = state(
            stalled_minutes=20,
            recent_progress=0.0,
            strategy_effectiveness=0.1,
        )
        self.assertEqual(
            core.classify_struggle(value),
            "unproductive",
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "choice_prompt")
        self.assertIn(
            "continue_without_help",
            decision["choices"],
        )

    def test_low_monitoring_accuracy_gets_monitoring_prompt(self):
        value = state(monitoring_accuracy=0.2)
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "monitoring_prompt")

    def test_low_strategy_progress_gets_strategy_prompt(self):
        value = state(
            strategy_effectiveness=0.2,
            recent_progress=0.25,
        )
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "strategy_prompt")

    def test_minimal_preference_defaults_to_silent(self):
        value = state(support_preference="minimal")
        decision = core.decide_support(value)
        self.assertEqual(decision["action"], "silent_monitor")

    def test_render_support_has_distinct_prompt(self):
        value = state(
            strategy_effectiveness=0.2,
            recent_progress=0.25,
        )
        decision = core.decide_support(value)
        prompt = core.render_support(decision, value)
        self.assertIn("different strategy", prompt)

    def test_changed_strategy_updates_history(self):
        value = state(current_strategy="rereading")
        decision = {
            "action": "strategy_prompt",
        }
        updated = core.update_after_response(
            value,
            decision,
            "changed_strategy",
            next_strategy="worked example",
        )
        self.assertEqual(updated.previous_strategy, "rereading")
        self.assertEqual(updated.current_strategy, "worked example")
        self.assertEqual(updated.strategy_changes, 1)
        self.assertEqual(updated.support_count, 1)

    def test_changed_strategy_requires_next_strategy(self):
        with self.assertRaises(ValueError):
            core.update_after_response(
                state(),
                {"action": "strategy_prompt"},
                "changed_strategy",
            )

    def test_silent_monitor_does_not_increment_support_count(self):
        value = state()
        updated = core.update_after_response(
            value,
            {"action": "silent_monitor"},
            "not_applicable",
        )
        self.assertEqual(updated.support_count, value.support_count)

    def test_reflection_record_validation(self):
        with self.assertRaises(ValueError):
            core.ReflectionRecord(1.2, 0.5, 0.0)

    def test_reflection_can_close_goal(self):
        record = core.ReflectionRecord(
            strategy_usefulness=0.8,
            goal_progress_assessment=0.98,
            confidence_change=0.1,
        )
        result = core.adaptation_from_reflection(record)
        self.assertEqual(
            result["adaptation"],
            "close_goal_or_set_next",
        )

    def test_reflection_can_revise_strategy(self):
        record = core.ReflectionRecord(
            strategy_usefulness=0.2,
            goal_progress_assessment=0.5,
            confidence_change=0.0,
            next_strategy="practice retrieval",
        )
        result = core.adaptation_from_reflection(record)
        self.assertEqual(result["adaptation"], "revise_strategy")
        self.assertEqual(
            result["next_strategy"],
            "practice retrieval",
        )

    def test_reflection_can_flag_confidence_decline(self):
        record = core.ReflectionRecord(
            strategy_usefulness=0.7,
            goal_progress_assessment=0.5,
            confidence_change=-0.4,
        )
        result = core.adaptation_from_reflection(record)
        self.assertEqual(
            result["adaptation"],
            "review_evidence_and_seek_support",
        )

    def test_policy_trace_reports_zero_productive_interruptions(self):
        states = [
            state(),
            state(
                stalled_minutes=12,
                effort=0.9,
                recent_progress=0.4,
                strategy_effectiveness=0.8,
            ),
            state(
                learner_requested_help=True,
                stalled_minutes=20,
                recent_progress=0.0,
            ),
        ]
        report = core.evaluate_policy_trace(states)
        self.assertEqual(
            report["productive_struggle_interruptions"],
            0,
        )
        self.assertEqual(report["steps"], 3)

    def test_policy_trace_respects_opt_out(self):
        report = core.evaluate_policy_trace(
            [
                state(
                    support_preference="off",
                    stalled_minutes=20,
                    recent_progress=0.0,
                    strategy_effectiveness=0.1,
                )
            ]
        )
        self.assertEqual(report["preference_violations"], 0)
        self.assertEqual(report["prompt_rate"], 0.0)

    def test_policy_trace_requires_states(self):
        with self.assertRaises(ValueError):
            core.evaluate_policy_trace([])

    def test_legacy_support_level_maps_silent_to_monitor(self):
        self.assertEqual(core.support_level(state()), "monitor")

    def test_legacy_reflection_prompt_is_none_for_monitor(self):
        self.assertIsNone(core.reflection_prompt(state()))

    def test_interaction_diagnostics(self):
        rows = [
            {
                "decision": {
                    "action": "planning_prompt",
                    "interrupt": True,
                },
                "learner_response": "accepted",
            },
            {
                "decision": {
                    "action": "strategy_prompt",
                    "interrupt": True,
                },
                "learner_response": "changed_strategy",
            },
            {
                "decision": {
                    "action": "silent_monitor",
                    "interrupt": False,
                },
                "learner_response": "not_applicable",
            },
        ]
        result = core.interaction_diagnostics(rows)
        self.assertEqual(result["prompted_interactions"], 2)
        self.assertEqual(result["strategy_change_count"], 1)
        self.assertEqual(
            result["engaged_response_fraction_among_prompts"],
            1.0,
        )

    def test_interaction_diagnostics_validates_response(self):
        with self.assertRaises(ValueError):
            core.interaction_diagnostics(
                [
                    {
                        "decision": {
                            "action": "planning_prompt",
                            "interrupt": True,
                        },
                        "learner_response": "mystery",
                    }
                ]
            )


if __name__ == "__main__":
    unittest.main()
