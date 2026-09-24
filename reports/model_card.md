# Analytic system card

## System

Self-Regulated Learning Copilot

## Purpose

Transparent, agency-preserving support policy for planning, monitoring, strategy adaptation, help choice, guided hints, reflection, and next-cycle adaptation.

## Current maturity

Working research prototype.

All bundled learner states, trajectories, responses, thresholds, and evaluation outputs are synthetic.

The repository demonstrates policy logic and evaluation structure. It does not establish educational effectiveness.

## Theoretical orientation

The design is informed by cyclical self-regulated learning models, especially recurring ideas involving:

- task context
- goals and plans
- strategies/tactics
- monitoring
- reflection/adaptation

The implementation is intentionally narrower than the full SRL construct.

## Inputs

The policy receives explicit state variables including:

- mastery
- confidence
- effort
- stalled time
- goal
- goal progress
- next action
- success evidence
- current/previous strategy
- strategy effectiveness
- strategy-change count
- recent progress
- monitoring accuracy
- learner-requested help
- support preference
- minutes since support
- support count
- reflection due
- task difficulty
- time pressure

The package does not infer these variables from raw learner traces.

## Support actions

The policy can return:

- `silent_monitor`
- `planning_prompt`
- `monitoring_prompt`
- `strategy_prompt`
- `choice_prompt`
- `guided_hint`
- `reflection_prompt`

Silent monitoring produces no learner-facing message.

## Learner control

The implementation includes:

- opt-out
- minimal-support preference
- explicit help request
- prompt cooldown
- prompt-count limit
- support choices
- decline responses

An explicit learner request for help can override passive suppression.

## Productive struggle

The policy includes an operational productive-struggle category based on supplied effort, recent progress, strategy effectiveness, and stall duration.

Productive struggle is not interrupted unless the learner asks for support.

This rule is a hypothesis for evaluation, not an empirically validated classifier.

## Reflection and adaptation

Learner-supplied reflection can produce an explicit next-cycle suggestion such as:

- close goal / set next goal
- revise strategy
- review evidence and seek support
- continue or refine strategy

The system does not infer hidden motivational causes.

## Diagnostics

The repository can report:

### Policy trace

- prompt rate
- silent-monitor rate
- action counts
- productive-struggle interruptions
- learner-preference violations

### Interaction responses

- response counts
- decline fraction
- engaged-response fraction
- strategy-change count

These are observable interaction metrics, not psychological assessments.

## Main limitations

The current system:

- uses supplied rather than estimated SRL state
- uses hand-authored thresholds
- does not learn from prior learners
- does not validate state variables
- does not estimate uncertainty
- does not infer task semantics
- does not generate personalized natural-language prompts
- does not estimate causal intervention effects
- does not measure long-term independent regulation
- does not establish that acceptance/compliance is beneficial

## Evidence needed before real use

A real study should provide:

- validated state-estimation procedure
- threshold sensitivity
- learner preference validation
- comparison with no-support and request-only baselines
- prompt-burden evaluation
- productive-struggle validation
- support appropriateness ratings
- learning outcomes
- learner agency/autonomy measures
- accessibility review
- privacy review
- longitudinal independence/dependency outcomes

## Human oversight

The policy is intended as an inspectable research instrument.

Learners should retain the ability to continue without help, decline support, and request support when they want it.

No output should be treated as a diagnosis of motivation, ability, or self-regulation quality.
