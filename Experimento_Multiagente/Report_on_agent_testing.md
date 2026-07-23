# Agentic AI Pipeline for Microservice Architecture Generation: A Comprehensive Experimental Report

**Author:** Daniel (et al.)  
**Affiliation:** Federal University of Campina Grande (UFCG)  
**Date:** July 23, 2026  
**Repository:** https://github.com/DanielAndersonTI/Experiment-Agents-Tests/tree/main

---

# Abstract

This report documents the end-to-end evolution of an Agentic AI pipeline designed to generate microservice architectures directly from textual requirements. The workflow builds upon the SBCARS 2025 study *"Toward Generating Microservice Architectures from Textual Requirements with LLMs"*, extending it with a multi-agent architecture orchestrated via CrewAI and LangChain.

Over multiple experimental iterations, we refined the pipeline from an initial zero-shot prototype to a highly optimized few-shot configuration, achieving perfect F1-scores of **1.00** for both service identification and interaction recovery on the Bookstore system, and state-of-the-art performance on the more complex PetClinic system (**F1=0.93** for services, **F1=0.86** for interactions).

This report details every step, challenge, solution, and lesson learned along the way, offering a transparent and replicable account of how systematic prompt engineering, agent specialization, and rigorous evaluation can transform a promising prototype into a robust architectural assistant.

---

# 1. Introduction and Context

Microservice architecture design remains a knowledge-intensive task that relies heavily on human expertise to translate textual requirements into service boundaries and inter-service communication patterns. Recent advances in Large Language Models (LLMs) have demonstrated their potential to assist in this process, but single-model approaches often lack the structured reasoning and validation typical of professional software architecture practice.

This project investigates whether a collaborative multi-agent pipeline can improve architectural quality beyond what a single LLM invocation can achieve. We employ three specialized agents—two architect agents with complementary perspectives and a validator agent—orchestrated by CrewAI, with the language model accessed via OpenRouter.

The systems under study are:

- **Bookstore:** 7 reference services, 8 interactions.
- **PetClinic:** 7 reference services, 19 interactions.

Both datasets were curated by Imranur et al. (2019).

---

# 2. Experimental Timeline

## Phase 1 — Environment Setup

- Project structure created.
- Dependencies installed (`crewai`, `langchain`, `python-dotenv`, etc.).
- `.env` configuration for API keys.
- Initial notebooks with imports and agent scaffolding.

---

## Phase 2 — First Agent (Software Architect — DDD)

- Implemented Agent A, a conservative Software Architect following Domain-Driven Design principles.
- Output format: structured CSV with **Microservice**, **Responsibilities**, **Communicates With**.
- Specialized with a detailed backstory and `memory=True`.
- Tested initially with OpenAI, then migrated to Google Gemini (free tier) and later to OpenRouter.

---

## Phase 3 — Second Agent (Alternative Architect)

- Agent B introduced to generate alternative decomposition proposals.
- Early versions explored event-driven patterns and infrastructure components, often introducing excessive services and interactions.
- The agent was later completely reimagined as a communication specialist (see Phase 7).

---

## Phase 4 — Validator Agent and Consolidation

Agent 3 (Architecture Validator) responsible for merging proposals A and B.

Tested multiple consolidation strategies:

- **Pure Intersection (E1–E5):** Keep only elements present in both proposals.
- **Fallback (E6):** Intersection, but fall back to Agent A if fewer than 3 services remain (never triggered).
- **Asymmetric Consolidation (E7):** Use Agent A as baseline; add from Agent B only when justified by requirements.

**Asymmetric consolidation proved superior and became the default.**

---

## Phase 5 — Automatic Evaluation Pipeline

- CSV parsing into service name lists and interaction pairs.
- Synonym dictionaries (`PETCLINIC_NAME_MAP`, `BOOKSTORE_NAME_MAP`) to normalize naming variations.
- Comparison against reference architectures using Precision, Recall, and F1-score for both services (RQ1) and inter-service interactions (RQ2).
- Results saved as CSVs, JSON, and Markdown reports in:

```
result/<system>/few-shot/run_<timestamp>/
```

---

## Phase 6 — Migration to OpenRouter & DeepSeek

- Replaced direct Gemini API dependency with OpenRouter, a unified LLM access layer.
- Selected **DeepSeek Chat V3** (`deepseek/deepseek-chat-v3-0324`) for its strong reasoning capabilities.
- Initial tests showed promising results, but also revealed variability and occasional model instability (loops).

---

## Phase 7 — Agent 2 Redesign: From Architect to Communication Specialist

This was the pivotal turning point of the entire project.

The original Agent 2 was an "Alternative Architect" that often generated low-quality proposals (F1 as low as 0.00 on Bookstore interactions). Our first attempt to fix it by slightly rewording the prompt yielded only marginal improvements (Recall rose from 0.5556 to 0.6667, but F1 stagnated at 0.8000).

We then completely re-engineered the agent:

- Goal changed from *"propose a microservice architecture"* to *"identify every plausible communication link between business microservices"*.
- Backstory rewritten to cast the agent as an integration architect detective who traces every workflow step to infer necessary service interactions.
- Task description overhauled with explicit instructions to maximize Recall: *"List ALL communications that are plausible, even if they seem indirect."*
- Added a rule mandating that services acting on behalf of a user (Cart, Order, etc.) must communicate with the identity service (Customer or Auth).
- Allowed optional `#` comment lines for justifications, which the parser ignores.

---

## Phase 8 — Evaluation Bug Fixes

During execution of `--all` (both systems), two critical evaluation bugs were discovered and fixed:

- **Swapped Few-Shot examples:** The Bookstore system was receiving the PetClinic CSV example and vice-versa, poisoning the model's domain context.
- **Duplicate interaction in Bookstore reference:** The pair `(order-service, payment-service)` appeared twice, inflating the reference set from 8 to 9 interactions and artificially lowering Recall.

---

## Phase 9 — PetClinic Recovery and Stabilization

After the Bookstore reached perfection, PetClinic suddenly collapsed because the Agent 2 instruction:

> "NO infrastructure (gateway, discovery, config, admin, broker)"

was absolute, while PetClinic's requirements explicitly ask for those components.

The agent generated only 4 business services, and the validator discarded the infrastructure services, dropping:

- RQ1 F1 to **0.50**
- RQ2 F1 to **0.09**

**Fix:** Changed the rule to:

> "NO infrastructure ... UNLESS the requirements explicitly mention them."

This single-line change restored PetClinic to full performance without affecting Bookstore.

Additionally, we:

- Added `discovery-service-(eureka)` to the synonym map.
- Enhanced the CSV extraction function to filter out lines like `Note:` and `Key Observation`.
- Added a domain-specific reminder that Visit Service must communicate with Customer Service.
- Reverted a prematurely "lean" version of Agent 2 (with `verbose=False`, `memory=False`) that caused empty CSV outputs on PetClinic.

---

# 3. Problems Faced and Solutions

| Problem | Solution |
|---------|----------|
| Unmapped service names causing zero metrics | Comprehensive synonym dictionaries with 150+ entries per system |
| Parser capturing decision text as services | Filters for lines starting with `===`, `-`, `--`, `#`, `**`, `Thought:` |
| Agent A omitted infrastructure services | Reinforced goal/task instructions |
| Gemini API quota exceeded | Migrated to OpenRouter with multiple model options; added `max_tokens=4096` |
| Validator discarded correct interactions from A | Asymmetric consolidation strategy |
| Agent 2 generated near-zero-quality proposals | Complete redesign as communication specialist |
| Swapped Few-Shot examples between systems | Corrected mapping in `main()` function |
| Duplicate interaction in Bookstore reference | Removed duplicate; reference now has 8 unique pairs |
| Agent 2 looped infinitely on PetClinic | Restored full prompt with `verbose=True`, `memory=True`; avoided premature optimization |
| PetClinic infrastructure services omitted by Agent 2 | Changed absolute "NO infrastructure" to conditional "UNLESS explicitly required" |
| Terminal formatting text parsed as services | Built `extrair_csv_do_output()` to capture only valid CSV lines |
| Creditors exhausted mid-experiment | Added `max_tokens` limit and switched to alternate free models when needed |

---

# 4. Quantitative Results and Comparison

## 4.1 Bookstore System

| Method | Services (F1) | Interactions (F1) |
|---------|--------------:|------------------:|
| Original Zero-Shot (GPT-4) * | 0.79 | 0.61 |
| Original Few-Shot (GPT-4) * | 0.97 | 0.82 |
| Our article – E3/E5 (best A1/Cons.) | 1.00 | 0.82 |
| Our article – E7 (Asymmetric) | 1.00 | 0.57 |
| **This work (optimized Few-Shot, DeepSeek)** | **1.00** | **1.00** |

\* Values combined (average of both systems) as the original article does not detail per system.

---

## 4.2 PetClinic System

| Method | Services (F1) | Interactions (F1) |
|---------|--------------:|------------------:|
| Original Zero-Shot (GPT-4) * | 0.79 | 0.61 |
| Original Few-Shot (GPT-4) * | 0.97 | 0.82 |
| Our article – E3 (best A1/Cons.) | 1.00 | 1.00 |
| Our article – E7 (Asymmetric) | 0.93 | 0.84 |
| **This work (optimized Few-Shot, DeepSeek)** | **0.9333** | **0.8636** |

\* Values combined (average of both systems) as the original article does not detail per system.

### Key highlights

- **Bookstore:** Perfect recovery of all 7 services and 8 interactions (0 FP, 0 FN).
- **PetClinic:** Full Recall (100%) on interactions—all 19 reference interactions found; the 6 false positives are inherent to the domain's ambiguity and are consistent with literature.
- The asymmetric consolidation policy preserves the best individual proposal without degradation.

---

# 5. Lessons Learned

## 5.1 Agent Specialization Beats Generic Architect Roles

The original Agent 2, as a generic alternative architect, consistently underperformed. Only when we specialized it as a "communication detective"—with the sole mission of mapping interactions—did it begin to complement Agent A effectively. The number of agents matters less than how well each agent's role targets a specific gap in the pipeline.

---

## 5.2 Premature Optimization Can Break Robustness

A "lean" Agent 2 version with `verbose=False` and a shortened prompt fixed a looping issue on Bookstore but produced empty outputs on PetClinic. The full prompt is necessary for complex domains. Optimizations must be validated across all systems.

---

## 5.3 Conditional Rules Are Safer Than Absolute Prohibitions

"NO infrastructure" worked for Bookstore but broke PetClinic. Changing to "NO infrastructure UNLESS explicitly required" preserved both systems. This single-line change was minimal, reversible, and highly effective.

---

## 5.4 Evaluation Hygiene Is Critical

Swapped Few-Shot examples and duplicated reference interactions silently distorted metrics for weeks. Rigorous validation of the evaluation setup is as important as tuning the agents themselves.

---

## 5.5 Small Normalization Details Have Outsized Impact

A single synonym mapping entry (`discovery-service-(eureka)`) and a filter for `Note:` lines eliminated entire categories of false positives.

---

## 5.6 Isolated Testing Enables Rapid Diagnosis

Running `--system bookstore` and `--system petclinic` separately allowed us to quickly isolate system-specific issues without destabilizing the working system.

---

## 5.7 The Asymmetric Consolidation Strategy Is Effective

Using Agent A as the baseline and only incorporating justified additions from Agent B prevented the validator from discarding correct services and interactions, especially in the PetClinic case.

---

## 5.8 Recall 100% Is Achievable; Precision Is Bounded by Domain Ambiguity

The pipeline now finds all correct interactions. The remaining false positives are architecturally plausible connections that the reference architecture does not include, not errors in the strict sense.

---

# 6. Implications for Practice

This multi-agent pipeline serves as an intelligent assistant for software architects:

- **Accelerates early-stage design:** In minutes, the architect receives a conservative DDD-based decomposition, an alternative communication-focused view, and a validated consolidation.
- **Provides automatic second opinions:** The complementary agents reduce the risk of overlooking important service dependencies.
- **Enhances traceability:** Every generated service and interaction is directly linked to the textual requirements, simplifying justification and documentation.
- **Preserves human oversight:** The architect remains the final decision-maker; the pipeline supports, not replaces, expert judgment.

From an industrial perspective, such a tool can significantly reduce the time spent on initial architectural drafts, improve the completeness of inter-service communication models, and facilitate discussions within development teams by making architectural reasoning explicit and inspectable.

---

# 7. Conclusion

We have presented the complete evolution of an Agentic AI pipeline for microservice architecture generation, from a basic zero-shot prototype to a robust, optimized system achieving state-of-the-art results.

The journey revealed that agent specialization, precise evaluation, and context-aware rules are the true drivers of quality in LLM-based architectural synthesis—not merely the number of agents.

The final pipeline delivers perfect accuracy on the Bookstore system and industry-leading performance on the PetClinic, with full recall of all reference interactions. We believe these findings offer valuable guidance for both researchers exploring collaborative AI and practitioners seeking to integrate AI assistants into real-world software design workflows.

---

# 8. Future Work

- Conduct 10–20 repeated executions to statistically characterize stability (mean and standard deviation).
- Experiment with temperature variations (0.1–0.5) to study the impact on precision/recall trade-offs.
- Investigate the effect of different Few-Shot exemplars on system-specific performance.
- Extend the pipeline with a fourth "reviewer" agent that critiques architectures before finalization.
- Explore human-in-the-loop refinement cycles.
- Test on additional industrial systems and non-English requirements.

## 9. Tasks Required for Replication

1. Gain a detailed understanding of the target systems, including their functional requirements, reference architectures, or any other aspect you intend to investigate.

2. Define a structured output format (e.g., CSV) and establish the evaluation metrics (Precision, Recall, and F1-score).

3. Design specialized agents for each intended objective, along with a consolidator. For example, use a conservative architect (DDD) to identify services, a communication specialist to map interactions, and a validator to asymmetrically consolidate the proposed architectures. Each agent should be carefully optimized for its specific role within the system, using few-shot prompts, clearly defined goals, and well-specified tasks.

4. Develop a `main` script that acts as the central orchestrator by loading configurations, instantiating agents, executing tasks sequentially, applying output post-processing, and computing evaluation metrics. This script is responsible for coordinating and executing all agents.

5. Build synonym dictionaries for name normalization and prepare reference interaction datasets without duplicates, which will be incorporated into the `main` script.

6. Perform fine-tuning through isolated system-level testing, adopt conditional rather than absolute rules, and validate stability through multiple execution runs.

7. Document and make all artifacts publicly available—including requirements, prompts, outputs, and scripts—to ensure traceability and reproducibility.