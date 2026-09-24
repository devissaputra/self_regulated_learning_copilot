import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_regulated_learning_copilot.core import (
    ReflectionRecord,
    SRLState,
    adaptation_from_reflection,
    decide_support,
    evaluate_policy_trace,
    render_support,
    update_after_response,
)


def boolean(value):
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ValueError(f"invalid boolean: {value}")


def optional(value):
    value = value.strip()
    return value or None


def load_trajectories():
    grouped = defaultdict(list)
    with (ROOT / "data" / "sample.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            learner = row["learner"]
            state = SRLState(
                mastery=float(row["mastery"]),
                confidence=float(row["confidence"]),
                effort=float(row["effort"]),
                stalled_minutes=float(row["stalled_minutes"]),
                goal=optional(row["goal"]),
                goal_progress=float(row["goal_progress"]),
                next_action=optional(row["next_action"]),
                success_evidence=optional(row["success_evidence"]),
                current_strategy=optional(row["current_strategy"]),
                previous_strategy=optional(row["previous_strategy"]),
                strategy_effectiveness=float(
                    row["strategy_effectiveness"]
                ),
                strategy_changes=int(row["strategy_changes"]),
                recent_progress=float(row["recent_progress"]),
                monitoring_accuracy=float(
                    row["monitoring_accuracy"]
                ),
                learner_requested_help=boolean(
                    row["learner_requested_help"]
                ),
                support_preference=row["support_preference"],
                minutes_since_support=float(
                    row["minutes_since_support"]
                ),
                support_count=int(row["support_count"]),
                reflection_due=boolean(row["reflection_due"]),
                task_difficulty=float(row["task_difficulty"]),
                time_pressure=float(row["time_pressure"]),
            )
            grouped[learner].append(
                {
                    "step": int(row["step"]),
                    "state": state,
                    "learner_response": row["learner_response"],
                    "next_strategy": optional(row["next_strategy"]),
                }
            )
    return grouped


trajectories = load_trajectories()

print("Self-Regulated Learning Copilot synthetic demo")
print()

all_states = []
for learner, rows in sorted(trajectories.items()):
    rows.sort(key=lambda item: item["step"])
    states = [row["state"] for row in rows]
    all_states.extend(states)
    report = evaluate_policy_trace(states)

    print(learner)
    for row in rows:
        decision = decide_support(row["state"])
        prompt = render_support(decision, row["state"])
        print(
            " ",
            row["step"],
            {
                "action": decision["action"],
                "reason": decision["reason"],
                "interrupt": decision["interrupt"],
                "prompt": prompt,
                "learner_response": row["learner_response"],
            },
        )

        if row["learner_response"] == "changed_strategy":
            updated = update_after_response(
                row["state"],
                decision,
                row["learner_response"],
                next_strategy=row["next_strategy"],
            )
            print(
                "   strategy update:",
                {
                    "previous": updated.previous_strategy,
                    "current": updated.current_strategy,
                    "changes": updated.strategy_changes,
                },
            )

    print(
        " trajectory diagnostics:",
        {
            "prompt_rate": round(report["prompt_rate"], 3),
            "productive_struggle_interruptions": report[
                "productive_struggle_interruptions"
            ],
            "preference_violations": report[
                "preference_violations"
            ],
            "action_counts": report["action_counts"],
        },
    )

overall = evaluate_policy_trace(all_states)
print("\nOverall policy diagnostics:")
print(
    {
        "steps": overall["steps"],
        "prompted_steps": overall["prompted_steps"],
        "silent_steps": overall["silent_steps"],
        "prompt_rate": round(overall["prompt_rate"], 3),
        "productive_struggle_interruptions": overall[
            "productive_struggle_interruptions"
        ],
        "preference_violations": overall[
            "preference_violations"
        ],
        "action_counts": overall["action_counts"],
    }
)

reflection = ReflectionRecord(
    strategy_usefulness=0.30,
    goal_progress_assessment=0.62,
    confidence_change=-0.05,
    what_worked="Worked examples clarified the first step.",
    next_strategy="retrieval practice",
)
print(
    "\nReflection-driven adaptation example:",
    adaptation_from_reflection(reflection),
)

print(
    "\nNote: all states, thresholds, responses, and diagnostics are "
    "synthetic. The policy is transparent and agency-preserving by design, "
    "but its thresholds and educational effects require empirical validation."
)
