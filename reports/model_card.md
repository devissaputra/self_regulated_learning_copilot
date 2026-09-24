# Analytic system card

## System

Self-Regulated Learning Copilot

## Purpose

Rule based support policy for planning, monitoring, reflection, and guided hints from an explicit learner state.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces one support action and a corresponding learner facing prompt. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Validate the state representation separately from the intervention policy. Then compare policy variants on learner outcomes, intervention frequency, agency, and cases where the system interrupts productive work.

## Main limitation

The state values are supplied directly and the thresholds are design assumptions. This baseline cannot infer self regulation, motivation, or mental state from learner behavior.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
