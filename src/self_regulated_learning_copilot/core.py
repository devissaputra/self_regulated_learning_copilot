import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from numbers import Real


SUPPORT_ACTIONS = {
    "silent_monitor",
    "planning_prompt",
    "monitoring_prompt",
    "strategy_prompt",
    "choice_prompt",
    "guided_hint",
    "reflection_prompt",
}

SUPPORT_PREFERENCES = {"normal", "minimal", "off"}
LEARNER_RESPONSES = {
    "accepted",
    "declined",
    "continued_without_help",
    "requested_more_help",
    "changed_strategy",
    "completed_reflection",
    "not_applicable",
}


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _unit_interval(value, name):
    value = _finite_number(value, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def _nonnegative(value, name):
    value = _finite_number(value, name)
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def _nonnegative_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def _optional_text(value, name):
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string or None")
    return value.strip()


@dataclass(frozen=True)
class PolicyConfig:
    """Inspectable thresholds for the conservative support policy."""

    mild_stall_minutes: float = 8.0
    hint_stall_minutes: float = 15.0
    cooldown_minutes: float = 20.0
    maximum_support_count: int = 4
    low_progress: float = 0.20
    productive_progress: float = 0.20
    low_monitoring_accuracy: float = 0.35
    low_strategy_effectiveness: float = 0.35
    productive_strategy_effectiveness: float = 0.55
    high_effort: float = 0.60
    goal_completion: float = 0.95
    minimum_plan_completeness: float = 0.75

    def __post_init__(self):
        for name in (
            "mild_stall_minutes",
            "hint_stall_minutes",
            "cooldown_minutes",
        ):
            object.__setattr__(
                self,
                name,
                _nonnegative(getattr(self, name), name),
            )
        if self.hint_stall_minutes < self.mild_stall_minutes:
            raise ValueError(
                "hint_stall_minutes must be >= mild_stall_minutes"
            )
        _nonnegative_int(
            self.maximum_support_count,
            "maximum_support_count",
        )
        for name in (
            "low_progress",
            "productive_progress",
            "low_monitoring_accuracy",
            "low_strategy_effectiveness",
            "productive_strategy_effectiveness",
            "high_effort",
            "goal_completion",
            "minimum_plan_completeness",
        ):
            object.__setattr__(
                self,
                name,
                _unit_interval(getattr(self, name), name),
            )


@dataclass(frozen=True)
class SRLState:
    """Explicit SRL state supplied to the policy; no hidden state inference."""

    # Original four fields stay first for backward-compatible positional use.
    mastery: float
    confidence: float
    effort: float
    stalled_minutes: float

    # Forethought / planning.
    goal: str | None = None
    goal_progress: float = 0.0
    next_action: str | None = None
    success_evidence: str | None = None

    # Performance / strategy monitoring.
    current_strategy: str | None = None
    previous_strategy: str | None = None
    strategy_effectiveness: float = 0.5
    strategy_changes: int = 0
    recent_progress: float = 0.0
    monitoring_accuracy: float = 0.5

    # Learner control and intervention history.
    learner_requested_help: bool = False
    support_preference: str = "normal"
    minutes_since_support: float = 999.0
    support_count: int = 0
    reflection_due: bool = False

    # Task context. These are context descriptors, not learner traits.
    task_difficulty: float = 0.5
    time_pressure: float = 0.5

    def __post_init__(self):
        for name in (
            "mastery",
            "confidence",
            "effort",
            "goal_progress",
            "strategy_effectiveness",
            "recent_progress",
            "monitoring_accuracy",
            "task_difficulty",
            "time_pressure",
        ):
            object.__setattr__(
                self,
                name,
                _unit_interval(getattr(self, name), name),
            )

        object.__setattr__(
            self,
            "stalled_minutes",
            _nonnegative(self.stalled_minutes, "stalled_minutes"),
        )
        object.__setattr__(
            self,
            "minutes_since_support",
            _nonnegative(
                self.minutes_since_support,
                "minutes_since_support",
            ),
        )
        _nonnegative_int(self.support_count, "support_count")
        _nonnegative_int(
            self.strategy_changes,
            "strategy_changes",
        )

        for name in (
            "goal",
            "next_action",
            "success_evidence",
            "current_strategy",
            "previous_strategy",
        ):
            object.__setattr__(
                self,
                name,
                _optional_text(getattr(self, name), name),
            )

        if not isinstance(self.learner_requested_help, bool):
            raise ValueError("learner_requested_help must be boolean")
        if not isinstance(self.reflection_due, bool):
            raise ValueError("reflection_due must be boolean")
        if self.support_preference not in SUPPORT_PREFERENCES:
            raise ValueError(
                "support_preference must be one of "
                f"{sorted(SUPPORT_PREFERENCES)}"
            )


@dataclass(frozen=True)
class ReflectionRecord:
    """Learner-supplied reflection used to plan the next SRL cycle."""

    strategy_usefulness: float
    goal_progress_assessment: float
    confidence_change: float
    what_worked: str | None = None
    next_strategy: str | None = None

    def __post_init__(self):
        object.__setattr__(
            self,
            "strategy_usefulness",
            _unit_interval(
                self.strategy_usefulness,
                "strategy_usefulness",
            ),
        )
        object.__setattr__(
            self,
            "goal_progress_assessment",
            _unit_interval(
                self.goal_progress_assessment,
                "goal_progress_assessment",
            ),
        )
        confidence_change = _finite_number(
            self.confidence_change,
            "confidence_change",
        )
        if not -1.0 <= confidence_change <= 1.0:
            raise ValueError(
                "confidence_change must be between -1 and 1"
            )
        object.__setattr__(
            self,
            "confidence_change",
            confidence_change,
        )
        object.__setattr__(
            self,
            "what_worked",
            _optional_text(self.what_worked, "what_worked"),
        )
        object.__setattr__(
            self,
            "next_strategy",
            _optional_text(self.next_strategy, "next_strategy"),
        )


def plan_completeness(state: SRLState) -> float:
    """Fraction of explicit planning elements currently present."""
    fields = (
        state.goal,
        state.next_action,
        state.success_evidence,
        state.current_strategy,
    )
    return sum(value is not None for value in fields) / len(fields)


def classify_struggle(
    state: SRLState,
    config: PolicyConfig | None = None,
) -> str:
    """Distinguish productive, unproductive, ambiguous, and no-stall states."""
    config = PolicyConfig() if config is None else config
    if not isinstance(config, PolicyConfig):
        raise ValueError("config must be a PolicyConfig")

    if state.stalled_minutes < config.mild_stall_minutes:
        return "not_stalled"

    productive = (
        state.effort >= config.high_effort
        and state.recent_progress >= config.productive_progress
        and state.strategy_effectiveness
        >= config.productive_strategy_effectiveness
    )
    if productive:
        return "productive"

    unproductive = (
        state.stalled_minutes >= config.hint_stall_minutes
        and state.recent_progress < config.low_progress
        and state.strategy_effectiveness
        < config.low_strategy_effectiveness
    )
    if unproductive:
        return "unproductive"

    return "ambiguous"


def _decision(
    action,
    reason,
    *,
    interrupt,
    intensity,
    choices=None,
):
    if action not in SUPPORT_ACTIONS:
        raise ValueError(f"unknown support action: {action}")
    return {
        "action": action,
        "reason": reason,
        "interrupt": bool(interrupt),
        "intensity": intensity,
        "choices": [] if choices is None else list(choices),
    }


def decide_support(
    state: SRLState,
    config: PolicyConfig | None = None,
):
    """Choose conservative SRL support while preserving learner control."""
    if not isinstance(state, SRLState):
        raise ValueError("state must be an SRLState")
    config = PolicyConfig() if config is None else config
    if not isinstance(config, PolicyConfig):
        raise ValueError("config must be a PolicyConfig")

    # Learner preference is checked first. Explicit help requests may override
    # a passive preference because the learner is actively asking for support.
    if (
        state.support_preference == "off"
        and not state.learner_requested_help
    ):
        return _decision(
            "silent_monitor",
            "learner_opted_out",
            interrupt=False,
            intensity=0,
        )

    if (
        state.minutes_since_support < config.cooldown_minutes
        and not state.learner_requested_help
    ):
        return _decision(
            "silent_monitor",
            "support_cooldown",
            interrupt=False,
            intensity=0,
        )

    if (
        state.support_count >= config.maximum_support_count
        and not state.learner_requested_help
    ):
        return _decision(
            "silent_monitor",
            "prompt_burden_limit",
            interrupt=False,
            intensity=0,
        )

    if (
        state.reflection_due
        or state.goal_progress >= config.goal_completion
    ):
        return _decision(
            "reflection_prompt",
            "goal_cycle_ready_for_reflection",
            interrupt=True,
            intensity=1,
            choices=("reflect_now", "later", "decline"),
        )

    if state.learner_requested_help:
        if (
            state.stalled_minutes >= config.hint_stall_minutes
            or state.recent_progress < config.low_progress
        ):
            return _decision(
                "guided_hint",
                "learner_requested_help_during_stall",
                interrupt=True,
                intensity=3,
                choices=("show_hint", "strategy_check", "decline"),
            )
        return _decision(
            "choice_prompt",
            "learner_requested_help",
            interrupt=True,
            intensity=1,
            choices=("strategy_check", "guided_hint", "continue"),
        )

    completeness = plan_completeness(state)
    if (
        completeness < config.minimum_plan_completeness
        and state.goal_progress < config.goal_completion
        and state.recent_progress < 0.40
    ):
        return _decision(
            "planning_prompt",
            "incomplete_plan_with_limited_progress",
            interrupt=True,
            intensity=1,
            choices=("plan_now", "continue", "decline"),
        )

    struggle = classify_struggle(state, config)
    if struggle == "productive":
        return _decision(
            "silent_monitor",
            "productive_struggle",
            interrupt=False,
            intensity=0,
        )

    if struggle == "unproductive":
        return _decision(
            "choice_prompt",
            "possible_unproductive_persistence",
            interrupt=True,
            intensity=1,
            choices=(
                "continue_without_help",
                "strategy_check",
                "guided_hint",
            ),
        )

    if (
        state.monitoring_accuracy
        < config.low_monitoring_accuracy
    ):
        return _decision(
            "monitoring_prompt",
            "monitoring_evidence_unclear",
            interrupt=True,
            intensity=1,
            choices=("review_evidence", "continue", "decline"),
        )

    if (
        state.strategy_effectiveness
        < config.low_strategy_effectiveness
        and state.recent_progress < 0.40
    ):
        return _decision(
            "strategy_prompt",
            "current_strategy_not_showing_progress",
            interrupt=True,
            intensity=2,
            choices=("change_strategy", "continue", "request_hint"),
        )

    if state.support_preference == "minimal":
        return _decision(
            "silent_monitor",
            "minimal_support_preference",
            interrupt=False,
            intensity=0,
        )

    return _decision(
        "silent_monitor",
        "no_support_needed",
        interrupt=False,
        intensity=0,
    )


def render_support(decision, state: SRLState):
    """Return learner-facing support; silent monitoring returns None."""
    if not isinstance(decision, Mapping):
        raise ValueError("decision must be a mapping")
    action = decision.get("action")
    if action not in SUPPORT_ACTIONS:
        raise ValueError("decision contains an unknown action")
    if not isinstance(state, SRLState):
        raise ValueError("state must be an SRLState")

    if action == "silent_monitor":
        return None

    prompts = {
        "planning_prompt": (
            "What is your next concrete action, and what evidence will "
            "show that you made progress?"
        ),
        "monitoring_prompt": (
            "What evidence from your work tells you whether your current "
            "approach is working?"
        ),
        "strategy_prompt": (
            "Your current approach is not showing much progress. Would "
            "you like to try a different strategy, continue, or ask for a hint?"
        ),
        "choice_prompt": (
            "Would you like more time, a strategy check, or a guided hint?"
        ),
        "guided_hint": (
            "What is the smallest part of the task you can explain with "
            "confidence? Start there, then choose whether you want another hint."
        ),
        "reflection_prompt": (
            "What strategy helped, what evidence shows progress, and what "
            "would you keep or change for the next goal?"
        ),
    }
    return prompts[action]


def update_after_response(
    state: SRLState,
    decision,
    learner_response,
    *,
    next_strategy=None,
):
    """Record a learner response without inferring hidden motivation."""
    if learner_response not in LEARNER_RESPONSES:
        raise ValueError(
            "learner_response must be one of "
            f"{sorted(LEARNER_RESPONSES)}"
        )
    if not isinstance(decision, Mapping):
        raise ValueError("decision must be a mapping")
    action = decision.get("action")
    if action not in SUPPORT_ACTIONS:
        raise ValueError("decision contains an unknown action")

    if action == "silent_monitor":
        support_increment = 0
    else:
        support_increment = 1

    updates = {
        "support_count": state.support_count + support_increment,
        "minutes_since_support": (
            state.minutes_since_support
            if support_increment == 0
            else 0.0
        ),
    }

    if learner_response == "changed_strategy":
        strategy = _optional_text(next_strategy, "next_strategy")
        if strategy is None:
            raise ValueError(
                "next_strategy is required when strategy changes"
            )
        updates.update(
            {
                "previous_strategy": state.current_strategy,
                "current_strategy": strategy,
                "strategy_changes": state.strategy_changes + 1,
            }
        )

    if learner_response == "completed_reflection":
        updates["reflection_due"] = False

    return replace(state, **updates)


def adaptation_from_reflection(record: ReflectionRecord):
    """Return a transparent next-cycle suggestion from learner reflection."""
    if not isinstance(record, ReflectionRecord):
        raise ValueError("record must be a ReflectionRecord")

    if record.goal_progress_assessment >= 0.95:
        return {
            "adaptation": "close_goal_or_set_next",
            "reason": "goal_reported_complete",
            "next_strategy": record.next_strategy,
        }
    if record.strategy_usefulness < 0.40:
        return {
            "adaptation": "revise_strategy",
            "reason": "strategy_reported_low_usefulness",
            "next_strategy": record.next_strategy,
        }
    if record.confidence_change <= -0.25:
        return {
            "adaptation": "review_evidence_and_seek_support",
            "reason": "confidence_declined_during_cycle",
            "next_strategy": record.next_strategy,
        }
    return {
        "adaptation": "continue_or_refine_strategy",
        "reason": "strategy_reported_useful",
        "next_strategy": record.next_strategy,
    }


def evaluate_policy_trace(
    states: Sequence[SRLState],
    *,
    config: PolicyConfig | None = None,
):
    """Run the transparent policy over a supplied longitudinal state sequence."""
    if not isinstance(states, Sequence) or isinstance(
        states, (str, bytes)
    ):
        raise ValueError("states must be a sequence")
    if not states:
        raise ValueError("states must not be empty")
    if not all(isinstance(state, SRLState) for state in states):
        raise ValueError("every state must be an SRLState")

    config = PolicyConfig() if config is None else config
    decisions = []
    action_counts = Counter()
    productive_interruptions = 0
    preference_violations = 0

    for index, state in enumerate(states):
        decision = decide_support(state, config)
        prompt = render_support(decision, state)
        struggle = classify_struggle(state, config)

        if (
            struggle == "productive"
            and decision["interrupt"]
            and not state.learner_requested_help
        ):
            productive_interruptions += 1

        if (
            state.support_preference == "off"
            and decision["interrupt"]
            and not state.learner_requested_help
        ):
            preference_violations += 1

        record = {
            "step": index,
            "decision": decision,
            "prompt": prompt,
            "struggle": struggle,
            "plan_completeness": plan_completeness(state),
        }
        decisions.append(record)
        action_counts[decision["action"]] += 1

    prompted = sum(
        record["decision"]["interrupt"]
        for record in decisions
    )
    silent = len(decisions) - prompted

    return {
        "steps": len(decisions),
        "prompted_steps": prompted,
        "silent_steps": silent,
        "prompt_rate": prompted / len(decisions),
        "productive_struggle_interruptions": productive_interruptions,
        "preference_violations": preference_violations,
        "action_counts": dict(sorted(action_counts.items())),
        "decisions": decisions,
    }


# Backward-compatible helpers from the original prototype.
def support_level(state: SRLState) -> str:
    action = decide_support(state)["action"]
    return "monitor" if action == "silent_monitor" else action


def reflection_prompt(state: SRLState):
    return render_support(decide_support(state), state)
