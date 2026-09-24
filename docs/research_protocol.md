# Research protocol

## Project

Self-Regulated Learning Copilot

## Research questions

1. How can explicit learner-state evidence support goal setting, planning, monitoring, strategy adaptation, and reflection without replacing learner control?
2. When should a support system remain silent because the learner is making productive progress?
3. When do planning, monitoring, strategy, choice, hint, or reflection supports become appropriate?
4. How do learner preferences, explicit help requests, recent support history, and prompt burden change the support decision?
5. Which policy thresholds are robust across tasks, learners, and contexts?
6. How should state-estimation quality be separated from intervention-policy quality?

## SRL framework

The design is informed by established cyclical models of self-regulated learning.

Panadero's review of major SRL models describes common recurring processes involving planning/forethought, performance and strategy use, monitoring, and reflection/adaptation.

Reference:

- Panadero, E. (2017). A Review of Self-regulated Learning: Six Models and Four Directions for Research. Frontiers in Psychology, 8, 422.
- https://doi.org/10.3389/fpsyg.2017.00422

The repository also follows the practical structure commonly associated with Winne and Hadwin's model:

1. task context / definition
2. goals and plans
3. tactics and strategies with monitoring
4. adaptation

The implementation is not claimed to reproduce any one theoretical model exactly.

## Current state representation

The policy receives an explicit `SRLState`.

It includes:

### Learning evidence

- mastery
- confidence
- effort
- stalled time
- recent progress

### Forethought and planning

- goal
- goal progress
- next action
- success evidence

### Strategy use and monitoring

- current strategy
- previous strategy
- strategy effectiveness
- strategy changes
- monitoring accuracy

### Learner control and intervention history

- learner-requested help
- support preference
- minutes since support
- support count
- reflection due

### Task context

- task difficulty
- time pressure

These variables are supplied to the policy.

The current code does **not** infer motivation, emotion, self-efficacy, mental state, or SRL quality from raw traces.

## Planning completeness

`plan_completeness()` checks whether four explicit planning elements are present:

- goal
- next action
- success evidence
- current strategy

This is a structural completeness indicator.

It is not a validated measure of planning quality.

## Productive vs potentially unproductive struggle

`classify_struggle()` distinguishes:

- not stalled
- productive
- ambiguous
- potentially unproductive

The classification uses supplied stall duration, effort, recent progress, and strategy effectiveness.

Productive struggle is explicitly protected from unsolicited prompts.

This operational rule requires empirical validation before real use.

## Conservative support policy

`decide_support()` can choose:

- silent monitoring
- planning prompt
- monitoring prompt
- strategy prompt
- learner choice prompt
- guided hint
- reflection prompt

The policy prioritizes learner control.

### Silent monitoring

Silent monitoring produces **no learner-facing prompt**.

It can occur when:

- no support appears necessary
- the learner opted out
- the learner recently received support
- the support-count limit has been reached
- the learner appears to be productively struggling
- the learner requested minimal support and no stronger trigger is present

### Help requests

An explicit learner request for help can override passive suppression rules such as opt-out or cooldown because the learner is actively asking for assistance.

### Choice before stronger intervention

Potentially unproductive persistence does not automatically trigger a hint.

The learner first receives a choice among continuing, checking strategy, or requesting a guided hint.

## Prompt burden

The policy includes:

- configurable cooldown
- configurable maximum support count
- silent monitoring
- explicit learner support preference

These are design protections against repeated interruption.

They are not validated optimal values.

## Reflection and adaptation

`ReflectionRecord` stores learner-supplied:

- strategy usefulness
- goal-progress assessment
- confidence change
- what worked
- possible next strategy

`adaptation_from_reflection()` produces a transparent next-cycle suggestion such as:

- close goal / set next goal
- revise strategy
- review evidence and seek support
- continue or refine strategy

The learner reflection remains the source of the information.

The software does not infer hidden reasons for the learner's response.

## Longitudinal policy evaluation

`evaluate_policy_trace()` runs the policy across a supplied state sequence and reports:

- prompted steps
- silent steps
- prompt rate
- action counts
- productive-struggle interruptions
- support-preference violations

`interaction_diagnostics()` summarizes observable support responses such as:

- accepted
- declined
- changed strategy
- completed reflection

These are interaction diagnostics, not measures of motivation.

## Empirical evaluation

A serious study should separate four questions.

### 1. State validity

Do the supplied or estimated state variables correspond to defensible SRL processes?

### 2. Trigger validity

Does the policy identify useful moments for support?

### 3. Support appropriateness

Is the selected support type suitable for the learner's context?

### 4. Learning and agency outcomes

Does support improve useful outcomes without increasing dependency or unnecessary interruption?

## Comparators

Useful baselines include:

- always silent
- fixed-time prompts
- learner-requested support only
- non-personalized prompts
- the transparent adaptive policy
- a stronger adaptive alternative if justified

## Evaluation measures

Potential measures include:

- goal progress
- task performance
- strategy adaptation
- stall recovery
- support acceptance/decline
- prompt burden
- productive-struggle interruption rate
- learner preference violations
- reflection completion
- learner-reported usefulness
- perceived autonomy / control

A real study should predefine which outcomes matter before examining results.

## Threshold sensitivity

All current policy thresholds are design assumptions.

An empirical study should evaluate reasonable threshold ranges rather than treating one configuration as theoretically correct.

## Threats to validity

Important threats include:

- invalid state estimation
- course/task differences
- learner preference differences
- ambiguity in what counts as a strategy
- productive struggle being mistaken for failure
- recent progress being poorly measured
- support itself altering later state variables
- learner responses being interpreted too strongly
- prompt fatigue
- novelty effects
- repeated-measures dependence
- learners using support outside the instrumented environment
- state variables capturing task conditions rather than learner regulation

The central evaluation question is not whether the policy can produce prompts. It is whether those prompts are timely, useful, and sufficiently respectful of learner control.
