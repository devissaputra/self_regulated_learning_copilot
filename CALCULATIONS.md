# Calculation guide

## Question and evidence

When should support be offered, delayed or declined?

Supplied learning state, explicit plans, preferences, reflection and prompt history.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Check plan structure and struggle rules; respect learner choice and prompt burden; support reflection and adaptation.

## Calculation and interpretation

`Plan completeness = present planning fields / 4.`

The four fields are goal, next action, success evidence and strategy. Completeness is structural, not educational quality. State variables are supplied and the policy does not infer motivation or psychological status.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| planning fields present: 3 of 4 | 0.75 | unitless | `outputs.planning fields present: 3 of 4` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This transparent support policy uses supplied plans, progress, preferences, and interaction history to decide whether to offer help or remain silent. It preserves refusal and help requests, limits prompt burden, and links reflection to later strategy choices. The synthetic examples test policy behavior; structural plan completeness and struggle labels are operational rules rather than validated psychological assessments.

## Verification performed in this review

40 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`boolean`](scripts/run_demo.py#L20) | Inspect the explicit implementation and its callers. |
| [`optional`](scripts/run_demo.py#L29) | Inspect the explicit implementation and its callers. |
| [`load_trajectories`](scripts/run_demo.py#L34) | Inspect the explicit implementation and its callers. |
| [`plan_completeness`](src/self_regulated_learning_copilot/core.py#L274) | Fraction of explicit planning elements currently present. |
| [`classify_struggle`](src/self_regulated_learning_copilot/core.py#L285) | Distinguish productive, unproductive, ambiguous, and no-stall states. |
| [`decide_support`](src/self_regulated_learning_copilot/core.py#L337) | Choose conservative SRL support while preserving learner control. |
| [`render_support`](src/self_regulated_learning_copilot/core.py#L492) | Return learner-facing support; silent monitoring returns None. |
| [`update_after_response`](src/self_regulated_learning_copilot/core.py#L533) | Record a learner response without inferring hidden motivation. |
| [`adaptation_from_reflection`](src/self_regulated_learning_copilot/core.py#L586) | Return a transparent next-cycle suggestion from learner reflection. |
| [`evaluate_policy_trace`](src/self_regulated_learning_copilot/core.py#L616) | Run the transparent policy over a supplied longitudinal state sequence. |
| [`support_level`](src/self_regulated_learning_copilot/core.py#L685) | Inspect the explicit implementation and its callers. |
| [`reflection_prompt`](src/self_regulated_learning_copilot/core.py#L690) | Inspect the explicit implementation and its callers. |
| [`interaction_diagnostics`](src/self_regulated_learning_copilot/core.py#L694) | Summarize observable learner responses to support interactions. |

## What remains before a stronger research claim

The four fields are goal, next action, success evidence and strategy. Completeness is structural, not educational quality. State variables are supplied and the policy does not infer motivation or psychological status. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
