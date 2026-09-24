# Self-Regulated Learning Copilot

> Rule based support policy for planning, monitoring, reflection, and guided hints from an explicit learner state.

[![CI](https://github.com/devissaputra/self-regulated-learning-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/self-regulated-learning-copilot/actions/workflows/ci.yml)

![Self-Regulated Learning Copilot workflow](assets/architecture.svg)

**Area:** Learner Modeling & Self-Regulation    
**Status:** working research prototype  
**Author:** Devis Wawan Saputra

## What this project is for

This project explores adaptive support for self regulated learning without turning the system into an autopilot. An explicit learner state supplies mastery, confidence, effort, and stalled time to a small rule policy that chooses whether to monitor, prompt planning, offer a guided hint, or invite reflection.

**Who may find it useful:** Researchers and learning designers studying self-regulated learning, adaptive scaffolding, and learner agency.

## Research questions

1. How can trace-derived indicators support planning, monitoring, and reflection without replacing learner agency?
2. Which intervention rules reduce unproductive persistence while avoiding unnecessary interruption?
3. How should support intensity change as mastery, confidence, and effort evolve?

## How it works

The current copilot starts from an explicit state with mastery, confidence, effort, and stalled time. A small rule set chooses one of four support actions, and a second function returns the corresponding reflection or planning prompt. The code does not infer the state from raw traces.

![Self-Regulated Learning Copilot data and reasoning flow](assets/data_flow.svg)

The baseline path is learner state to support rule to support level to prompt. Keeping state estimation outside the module makes the intervention policy easy to audit on its own.

![Synthetic demo snapshot for Self-Regulated Learning Copilot](assets/demo_snapshot.svg)

This snapshot shows the bundled synthetic example for Self-Regulated Learning Copilot. It checks the software path; it is not an empirical performance result.

## Methods in the current baseline

- explicit learner state
- support rule policy
- guided hint trigger
- planning prompt trigger
- reflection prompt selection

## Data

Synthetic trace data are included. Real LMS or self regulation trace adapters are not bundled in this baseline.

`data/README.md` documents the sample schema and the conditions that should be recorded before any real dataset is connected. Restricted or identifiable learner data should stay outside the repository.

## Run the demo

```bash
git clone https://github.com/devissaputra/self-regulated-learning-copilot.git
cd self-regulated-learning-copilot
python scripts/run_demo.py
python -m unittest discover -s tests -v
```

The demo passes a low confidence, long stalled state into the policy and prints the guided hint action and learner prompt.

## What to evaluate next

The next step should separate state estimation quality from intervention quality. I would first validate the state variables, then compare the support policy with monitoring only and with a stronger adaptive alternative.

## Evaluation view

![Self-Regulated Learning Copilot evaluation dashboard](assets/evaluation_dashboard.svg)

The Self-Regulated Learning Copilot dashboard is an evaluation checklist rather than a result chart. The bars are illustrative only; the labels show the evidence a real study would need to collect.

## Limits and responsible use

The state values are supplied directly and the thresholds are design assumptions. This baseline cannot infer self regulation, motivation, or mental state from learner behavior. See `docs/ethics_and_risks.md` for the broader risk review.

## Repository map

```text
.
├── .github/workflows/ci.yml
├── assets/
│   ├── architecture.svg
│   ├── data_flow.svg
│   ├── demo_snapshot.svg
│   └── evaluation_dashboard.svg
├── data/
│   ├── README.md
│   └── sample.csv
├── docs/
│   ├── ethics_and_risks.md
│   ├── related_work.md
│   └── research_protocol.md
├── reports/model_card.md
├── scripts/run_demo.py
├── src/self_regulated_learning_copilot/core.py
├── tests/test_core.py
├── CITATION.cff
├── LICENSE
├── pyproject.toml
└── README.md
```

## Research path

A credible next version would:

1. define an observable and defensible state estimation procedure
2. compare support rules with a no intervention baseline
3. measure learner agency, recovery from stalls, and unwanted intervention

## Related work

`docs/related_work.md` points to open projects that are relevant to this problem area. They are context for comparison and study design; this repository does not present their code as its own.

## Citation and license

`CITATION.cff` contains the software citation. The code and original SVG visuals use the MIT License. Any external dataset keeps its own license and usage conditions.
