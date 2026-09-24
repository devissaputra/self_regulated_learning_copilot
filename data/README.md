# Data documentation

## Included data

`sample.csv` contains eight fully synthetic learner trajectories used to exercise the self-regulated learning support policy.

No real learner, LMS, instructor, or institution is represented.

The dataset is intentionally designed around **regulation states and support decisions**, not hidden psychological inference.

## SRL cycle represented

The synthetic schema separates several parts of a self-regulated learning cycle.

### Forethought and planning

- `goal`
- `goal_progress`
- `next_action`
- `success_evidence`

These fields make planning explicit rather than assuming that low effort means poor planning.

### Performance and strategy use

- `current_strategy`
- `previous_strategy`
- `strategy_effectiveness`
- `strategy_changes`
- `mastery`
- `confidence`
- `effort`
- `stalled_minutes`
- `recent_progress`
- `monitoring_accuracy`

The current code treats confidence as an explicit supplied learner-state signal. It does not infer motivation, self-efficacy, emotion, or mental state from behavior.

### Learner control

- `learner_requested_help`
- `support_preference`
- `minutes_since_support`
- `support_count`

Supported preferences are:

- `normal`
- `minimal`
- `off`

An explicit request for help can still produce support when the passive preference is `off`, because the learner is actively asking for assistance.

### Reflection and adaptation

- `reflection_due`
- `learner_response`
- `next_strategy`

The core package also contains a `ReflectionRecord` for learner-supplied strategy usefulness, perceived goal progress, confidence change, what worked, and a possible next strategy.

## Deliberate synthetic trajectories

The data include:

- L01: incomplete planning followed by plan formation and goal reflection
- L02: productive struggle that should not be interrupted
- L03: unproductive persistence, learner-requested help, and strategy change
- L04: learner opt-out followed by an explicit request for help
- L05: prompt cooldown and prompt-burden suppression
- L06: monitoring uncertainty followed by improved monitoring evidence
- L07: ineffective strategy followed by learner-selected strategy change
- L08: minimal-support preference and end-of-goal reflection

These are test scenarios, not learner archetypes.

## Important boundary

The repository does **not** estimate SRL state from raw clickstream data.

A real adapter would need to justify how observable events become state variables.

For example, `strategy_effectiveness=0.2` should never appear from an undocumented black-box transformation.

Every derived state should retain:

- source events
- observation window
- transformation rule/model
- uncertainty or confidence
- missing-data treatment
- course/task context
- timestamp/data-availability semantics

## Productive struggle

The synthetic policy distinguishes productive and potentially unproductive struggle using supplied effort, recent progress, strategy effectiveness, and stalled time.

This is an operational policy definition, not a universal psychological classification.

A real study must validate whether these indicators identify useful moments for support.

## Learner responses

The software supports explicit response categories such as:

- accepted
- declined
- continued_without_help
- requested_more_help
- changed_strategy
- completed_reflection
- not_applicable

These responses are behavioral records of interaction with the support system. They should not be interpreted as motivation or ability.

## Before real data are connected

Document:

- target population and learning context
- SRL framework used
- task definition
- goal representation
- strategy vocabulary
- state-estimation method
- support policy version
- threshold rationale
- learner preference/opt-out mechanism
- support cooldown
- intervention history
- prompt wording
- learner response semantics
- outcome measures
- missingness
- privacy/consent basis
- retention and access controls

## Do not commit

Do not commit identifiable learner traces, private messages, free-text reflections, grades, health/disability information, audio/video, restricted LMS exports, or proprietary course content.

Keep sensitive data outside Git and use an approved secure environment.
