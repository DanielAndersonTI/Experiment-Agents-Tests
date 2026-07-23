# Agentic AI Pipeline for Microservice Architecture Generation

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.28+-green.svg)](https://crewai.com/)
[![OpenRouter](https://img.shields.io/badge/LLM-DeepSeek%20Chat%20V3-orange.svg)](https://openrouter.ai/)

A multi-agent pipeline that generates complete microservice architectures — including service boundaries and inter-service communication links — directly from textual requirements. Built with **CrewAI**, **LangChain**, and **OpenRouter**, this project extends the SBCARS 2025 study *"Toward Generating Microservice Architectures from Textual Requirements with LLMs"* by introducing collaborative AI agents with complementary design perspectives and a structured validation process.

---

## Overview

Modern software architecture design remains a manual, knowledge-intensive task. Translating user stories into cohesive service boundaries and correct inter-service dependencies is time-consuming and error-prone. This project investigates whether an **Agentic AI workflow** — where multiple specialized agents collaborate and validate each other's outputs — can improve the quality of generated architectures beyond what a single LLM invocation can achieve.

### The Pipeline
User Stories (text)
│
▼
┌─────────────────────┐ ┌─────────────────────┐
│ Agent 1 (DDD) │ │ Agent 2 (Comm. │
│ Software Architect │ │ Specialist) │
│ Conservative, │ │ Exhaustive mapping │
│ precise boundaries │ │ of interactions │
└─────────┬───────────┘ └─────────┬───────────┘
│ Proposal A │ Proposal B
└──────────┬──────────────┘
▼
┌─────────────────────┐
│ Agent 3 │
│ Architecture │
│ Validator │
│ (Asymmetric │
│ Consolidation) │
└─────────┬───────────┘
▼
Final Microservice Architecture
│
▼
┌─────────────────────┐
│ Automatic │
│ Evaluation │
│ RQ1: Services │
│ RQ2: Interactions │
└─────────────────────┘

text

---

## Key Results

| System    | Services (F1) | Interactions (F1) | Interaction Recall |
|-----------|:-------------:|:-----------------:|:------------------:|
| Bookstore | **1.0000**    | **1.0000**        | 100% (8/8)         |
| PetClinic | **0.9333**    | **0.8636**        | 100% (19/19)       |

*Comparison with the original SBCARS 2025 study:*

| Method | Services (F1) | Interactions (F1) |
|--------|:-------------:|:----------------:|
| Zero-Shot (original, GPT-4) | 0.79 | 0.61 |
| Few-Shot (original, GPT-4) | 0.97 | 0.82 |
| **This work (Few-Shot, DeepSeek, multi-agent)** | **~0.97** | **~0.93** |

The multi-agent pipeline achieves **perfect recovery** on the simpler Bookstore system and **state-of-the-art performance** on the more complex PetClinic, with **100% recall on interactions** for both systems — meaning all expected communication links are correctly identified.

---

## Repository Structure
Experimento_Multiagente/
│
├── main_fewshot.py # Main orchestration script
├── agentes/ # Agent definitions
│ ├── agent1_architect_a_fs.py # Software Architect (DDD)
│ ├── agent2_architect_b_fs.py # Communication Specialist
│ └── agent3_validator_fs.py # Architecture Validator
│
├── result/ # Experiment results
│ ├── bookstore/few-shot/run_/
│ │ ├── proposta_a.csv
│ │ ├── proposta_b.csv
│ │ ├── consolidada.csv
│ │ ├── metricas_servicos.csv
│ │ ├── metricas_interacoes.csv
│ │ ├── sumario.json
│ │ └── report.md
│ └── petclinic/few-shot/run_/
│ └── ...
│
├── .env.example # API key template
├── requirements.txt # Python dependencies
└── README.md # This file

text

---

## Setup

### 1. Clone and create virtual environment

```bash
git clone <repository-url>
cd Experimento_Multiagente

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
2. Install dependencies
bash
pip install -r requirements.txt
3. Configure API credentials
bash
cp .env.example .env
Edit .env with your OpenRouter API key:

env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324
You can use any model available on OpenRouter by changing OPENROUTER_MODEL.

4. Run the experiment
bash
# Run on PetClinic only (default)
python main_fewshot.py

# Run on Bookstore only
python main_fewshot.py --system bookstore

# Run on both systems sequentially
python main_fewshot.py --all
Results will be saved in result/<system>/few-shot/run_<timestamp>/.

Agent Descriptions
Agent 1 — Software Architect (DDD)
Role: Conservative decomposition based on Domain-Driven Design

Strategy: Identifies only services explicitly supported by the requirements; avoids unnecessary infrastructure

Output: CSV with Microservice, Responsibilities, Communicates With

Agent 2 — Communication Specialist
Role: Exhaustive interaction mapper

Strategy: Uses the same business services as Agent 1, but produces a richer connectivity graph by tracing every workflow implied by the requirements

Key rule: Every user-triggered action must link the action service to the identity/authentication service

Infrastructure policy: Infrastructure services (gateway, discovery, config, admin) are included only if the requirements explicitly mention them

Agent 3 — Architecture Validator
Role: Asymmetric consolidator

Strategy: Uses Agent 1's proposal as the baseline; adds elements from Agent 2 only when they are justified by the requirements and do not introduce unnecessary complexity

Output: Consolidated CSV with an additional Source column (A, B, or A+B)

Evaluation Metrics
The generated architectures are compared against reference decompositions using:

RQ1 — Service Identification: Precision, Recall, F1-score for microservice boundaries

RQ2 — Interaction Recovery: Precision, Recall, F1-score for inter-service communication links

A comprehensive synonym dictionary normalizes naming variations (e.g., AuthenticationService → auth-service, EurekaServer → discovery-server) before comparison.

Experimental Evolution & Lessons Learned
Pivotal turning point: Redesigning Agent 2
The original Agent 2 was a generic "Alternative Architect" that performed poorly (F1 as low as 0.00 on interactions). A complete redesign transformed it into a communication specialist focused exclusively on mapping interactions. This single change, combined with evaluation bug fixes (swapped Few-Shot examples and duplicated reference interactions), drove the Bookstore system from F1≈0.80 to F1=1.00.

PetClinic recovery
PetClinic failed after the Bookstore optimizations because the instruction "NO infrastructure services" was absolute, while PetClinic's requirements explicitly mention API Gateway, Service Discovery, Config Server, and Admin Server. Changing to "NO infrastructure UNLESS the requirements explicitly mention them" — a single-line fix — restored full performance.

Key lessons
Agent specialization > agent count. The quality leap came from giving Agent 2 a precise, complementary role, not from adding more agents.

Conditional rules are safer than absolute prohibitions. Context-dependent instructions preserve robustness across different systems.

Evaluation hygiene matters. Bugs like swapped examples and duplicated references silently distorted metrics for weeks.

Small normalizations have outsized impact. One synonym mapping entry can eliminate an entire class of false positives.

Asymmetric consolidation works. Using the best proposal as a baseline and selectively incorporating complementary additions prevents degradation.

Implications for Practice
This pipeline serves as an intelligent assistant for software architects:

Accelerates early-stage design: Receive multiple architectural proposals in minutes instead of hours

Provides automatic second opinions: Reduces the risk of overlooking critical service dependencies

Enhances traceability: Every generated service and interaction is directly linked to textual requirements

Preserves human oversight: The architect remains the final decision-maker

Organizations adopting such workflows can expect faster design cycles, more complete inter-service communication models, and improved documentation — without replacing the creative and strategic role of the software architect.

Future Work
□ Statistical stability analysis over 10–20 repeated executions
□ Temperature sensitivity experiments (0.1–0.5 range)
□ Comparison across different LLM models (GPT-4, Gemini, Llama)
□ Human-in-the-loop refinement cycles
□ Extension to larger industrial systems and non-English requirements
References
Pereira, J. et al. (2025). Toward Generating Microservice Architectures from Textual Requirements with Large Language Models. SBCARS 2025.

Imranur, M. et al. (2019). A curated dataset of microservices-based systems. arXiv:1909.03249.

CrewAI Documentation: https://docs.crewai.com/

OpenRouter: https://openrouter.ai/

License
This project is shared for research and educational purposes. All artifacts are publicly available to ensure transparency and reproducibility.

For questions or collaboration, please open an issue or contact the authors.