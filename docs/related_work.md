# Related work and theoretical context

Self-Regulated Learning Copilot is an original transparent implementation.

It does not reproduce the models or empirical results below.

## Self-regulated learning models

Panadero reviewed six major models of self-regulated learning, including Zimmerman and Winne & Hadwin, and emphasized that SRL spans cognitive, metacognitive, motivational, behavioral, and contextual processes.

- Panadero, E. (2017)
- *A Review of Self-regulated Learning: Six Models and Four Directions for Research*
- Frontiers in Psychology, 8, 422
- https://doi.org/10.3389/fpsyg.2017.00422

This repository uses that literature as a reminder that SRL is broader than a single mastery or effort score.

## Winne and Hadwin cycle

A common description of Winne and Hadwin's model organizes SRL into recursive phases involving:

1. task definition
2. goals and plans
3. tactics and strategies
4. adaptation

Monitoring can occur across the process.

The current repository operationalizes only a small transparent subset of those ideas:

- explicit goals
- planning elements
- strategy use
- progress monitoring
- learner-controlled support
- reflection
- next-cycle adaptation

It does not claim theoretical completeness.

## Personalized SRL scaffolding

Van der Graaf and colleagues describe the design and evaluation of personalized digital scaffolds for self-regulated learning and highlight the importance of connecting detected SRL processes, scaffold timing/content, learner response, and outcomes.

- van der Graaf, J., Raković, M., Fan, Y., Lim, L., Singh, S., Bannert, M., Gašević, D., et al. (2023)
- *How to design and evaluate personalized scaffolds for self-regulated learning*
- Metacognition and Learning, 18, 783–810
- https://doi.org/10.1007/s11409-023-09361-y

This is especially relevant to the repository's separation of:

- state representation
- support policy
- learner choices/responses
- policy evaluation

## FLoRA

FLoRA is an open research ecosystem for analytics and AI support for self-regulated learning.

- https://github.com/Xinyu-Li/FLoRA

It is useful context for process-oriented SRL analytics and adaptive support.

This repository is deliberately much smaller and focuses on an auditable rule policy rather than reproducing FLoRA.

## Current scope

Implemented:

- explicit SRL state
- goals and planning elements
- strategy history
- progress/monitoring variables
- productive-struggle protection
- learner help requests
- learner support preferences
- cooldown and burden limits
- planning/monitoring/strategy/choice/hint/reflection actions
- learner-response updates
- reflection-driven adaptation
- longitudinal policy diagnostics
- interaction-response diagnostics

Not implemented:

- automatic SRL process detection
- log-pattern classification
- multimodal state estimation
- emotion recognition
- motivation inference
- learned intervention policy
- reinforcement learning
- LLM-generated prompts
- causal effects of support
- validated personalization
- production learner modeling

The current project is best understood as a transparent SRL scaffolding policy laboratory whose thresholds and educational effects still require empirical validation.
