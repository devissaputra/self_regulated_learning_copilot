from dataclasses import dataclass


@dataclass(frozen=True)
class SRLState:
    mastery: float
    confidence: float
    effort: float
    stalled_minutes: float

    def __post_init__(self):
        for name in ("mastery", "confidence", "effort"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.stalled_minutes < 0:
            raise ValueError("stalled_minutes must be non-negative")


def support_level(state: SRLState) -> str:
    """Return a conservative support action that leaves control with the learner."""
    if state.stalled_minutes >= 15 and state.confidence < 0.35:
        return "guided_hint"
    if state.effort < 0.30 and state.mastery < 0.60:
        return "planning_prompt"
    if state.mastery >= 0.80 and state.confidence >= 0.65:
        return "reflection_prompt"
    return "monitor"


def reflection_prompt(state: SRLState) -> str:
    """Map the selected support action to a short learner facing prompt."""
    prompts = {
        "guided_hint": "What is the smallest part of the task you can explain with confidence?",
        "planning_prompt": "What is your next concrete action, and what evidence will show progress?",
        "reflection_prompt": "What strategy worked, and where could you transfer it next?",
        "monitor": "What evidence tells you that your current strategy is working?",
    }
    return prompts[support_level(state)]
