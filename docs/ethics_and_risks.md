# Ethics, safety, and misuse risks

## Intended use

Self-Regulated Learning Copilot is a research prototype for studying transparent, learner-controlled digital scaffolding.

It is not a motivation detector, psychological assessment, autonomous tutor, grading system, or learner-ranking system.

## Learner control comes first

A support system for self-regulated learning can undermine the very regulation it is intended to support if it constantly decides what the learner should do.

The current policy therefore includes:

- real silent monitoring
- learner opt-out
- minimal-support preference
- explicit help requests
- learner choices before stronger support
- support cooldown
- support-count limits
- ability to decline a prompt

These design features should be preserved or improved in later versions.

## Over-scaffolding and dependency

Frequent support can reduce opportunities to plan, monitor, persist, and adapt independently.

A successful system should not maximize prompt frequency or compliance.

It should investigate whether learners increasingly regulate their own activity without requiring the system.

## Productive struggle

Difficulty is not automatically a problem.

A learner may be working hard, making progress, and using an effective strategy even while a task takes time.

The policy therefore protects an operational category of productive struggle from unsolicited interruption.

That category still requires empirical validation.

## Unproductive persistence

Long stall time does not prove that a learner is confused or needs a hint.

The current baseline uses a learner-choice prompt before an unsolicited guided hint.

A learner-requested hint is treated differently from an automatically imposed hint.

## State inference risk

The current package accepts explicit state values.

If a future system estimates these values from logs, sensor data, text, or model predictions, it must not hide uncertainty.

For example:

- low activity is not low motivation
- long time-on-task is not necessarily confusion
- low confidence is not incapability
- strategy switching is not necessarily poor regulation

Every inferred state should retain provenance and uncertainty.

## Motivation and mental-state inference

Do not use this system to infer:

- motivation
- personality
- anxiety
- depression
- attention disorders
- intelligence
- persistence as a character trait
- other psychological or medical conditions

The current confidence field is a supplied task-level state variable, not a clinical construct.

## Learner preference

An opt-out should be meaningful.

Do not silently re-enable unsolicited prompts because a learner's predicted risk increases.

The current policy only overrides an opt-out when the learner explicitly requests help.

## Prompt fatigue

Repeated prompts can become distracting, coercive, or easy to ignore.

Track:

- prompt count
- time since last prompt
- declines
- repeated dismissals
- support usefulness
- task stage

Cooldown should be evaluated empirically rather than assumed to be optimal.

## Reflection privacy

Free-text reflection can contain personal or sensitive information.

The prototype does not require free text for policy decisions.

If reflection text is collected in a real study:

- minimize collection
- restrict access
- define retention
- avoid reusing it for unrelated profiling
- do not expose it to instructors or other systems without a justified purpose

## Surveillance risk

SRL support should not become continuous behavioral surveillance.

Collect only evidence required for the research question.

Do not add webcam, keystroke, emotion, biometric, or private-message monitoring simply because those signals might improve prediction.

## Fairness and accessibility

Support triggers may behave differently for learners using:

- assistive technology
- alternative workflows
- offline materials
- slower connectivity
- different language strategies
- different study schedules

Subgroup evaluation may be appropriate when lawful and privacy-protective, but parity metrics alone do not establish fairness.

## Excluded uses

Do not use this prototype alone for:

- grading
- admissions
- discipline
- scholarship decisions
- employment decisions
- psychological diagnosis
- medical diagnosis
- academic-integrity enforcement
- covert surveillance
- mandatory personalized learning paths
- ranking learners by motivation, agency, or self-regulation

## Before a real-user study

Document:

- SRL framework
- state-estimation procedure
- uncertainty
- learner preference controls
- opt-out behavior
- support timing
- prompt wording
- cooldown
- burden limits
- intervention logging
- privacy controls
- accessibility review
- adverse-event / complaint handling
- rollback criteria

The goal is to support learner regulation without replacing it.
