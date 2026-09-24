# Research protocol

## Project

Self-Regulated Learning Copilot

## Questions

1. How can trace-derived indicators support planning, monitoring, and reflection without replacing learner agency?
2. Which intervention rules reduce unproductive persistence while avoiding unnecessary interruption?
3. How should support intensity change as mastery, confidence, and effort evolve?

## Baseline methods

- explicit learner state
- support rule policy
- guided hint trigger
- planning prompt trigger
- reflection prompt selection

## Evidence to collect

Start from the current transparent baseline and record every transformation needed to produce one support action and a corresponding learner facing prompt. Keep a clear boundary between synthetic demonstration data and any future empirical dataset.

## Validation

Validate the state representation separately from the intervention policy. Then compare policy variants on learner outcomes, intervention frequency, agency, and cases where the system interrupts productive work.

## What counts as a useful result

The next step should separate state estimation quality from intervention quality. I would first validate the state variables, then compare the support policy with monitoring only and with a stronger adaptive alternative.

## Threats to validity

State estimation error, fixed thresholds, subject differences, and learner preferences can all change whether an intervention is helpful.
