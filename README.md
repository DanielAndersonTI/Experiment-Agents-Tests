# Multiagent Microservice Architecture Generation

A multi‑agent framework that generates microservice‑oriented architectures directly from textual requirements using Large Language Models. The pipeline — built with [CrewAI](https://crewai.com) and [LangChain](https://langchain.com) — employs two architect agents (DDD‑based and event‑driven) and a validator agent to produce, compare, and consolidate architectural decompositions. The approach is evaluated on the **Spring PetClinic** and **Bookstore** systems, replicating and extending the study *“Toward Generating Microservice Architectures from Textual Requirements with LLMs”*.

The project supports both **Zero‑Shot** and **Few‑Shot** prompting strategies, includes a comprehensive evaluation of services (RQ1) and interactions (RQ2), and features an asymmetric consolidation mechanism that eliminates performance degradation caused by divergent agent outputs.

---

## 🧠 How It Works

1. **Agent 1 – Software Architect (DDD)** proposes a decomposition strictly aligned with functional requirements.
2. **Agent 2 – Alternative Architect (event‑driven)** proposes an alternative architecture using asynchronous communication and API Gateway patterns.
3. **Agent 3 – Architecture Validator** consolidates the two proposals. In its improved version, it uses **asymmetric consolidation**: it adopts all services and interactions from Agent 1 as a baseline, and only adds items from Agent 2 when they are consensus‑based or clearly grounded in the requirements without introducing extra infrastructure.

All agents receive the same textual requirements and output a CSV with services, responsibilities, and inter‑service communication. The generated architectures are automatically compared against reference architectures (ground truth) using **Precision**, **Recall**, and **F1‑Score**, for both services (RQ1) and interactions (RQ2). Reports are saved in Markdown, CSV, and JSON formats.

---

## 📁 Repository Structure
├── main.py # Zero‑Shot experiment script
├── main_fewshot.py # Few‑Shot experiment script
├── agentes/
│ ├── agent1_architect_a.py # DDD Architect (Zero‑Shot)
│ ├── agent1_architect_a_fs.py # DDD Architect (Few‑Shot)
│ ├── agent2_architect_b.py # Alternative Architect (Zero‑Shot)
│ ├── agent2_architect_b_fs.py # Alternative Architect (Few‑Shot)
│ ├── agent3_validator.py # Validator (Zero‑Shot)
│ ├── agent3_validator_fs.py # Validator (Few‑Shot, asymmetric consolidation)
│ └── init.py
├── result/
│ ├── petclinic/
│ │ ├── run_<timestamp>/ # Zero‑Shot runs
│ │ └── few-shot/
│ │ └── run_<timestamp>/ # Few‑Shot runs
│ └── bookstore/
│ ├── run_<timestamp>/ # Zero‑Shot runs
│ └── few-shot/
│ └── run_<timestamp>/ # Few‑Shot runs
├── .env.example
├── requirements.txt
├── historico_resultados_petclinic.md
├── contexto_e_proximos_passos.md
└── README.md

text

---

## ⚙️ Setup

1. **Clone the repository** and navigate to the project folder.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   venv\Scripts\activate.bat       # Windows (cmd)
   .\venv\Scripts\Activate.ps1     # Windows (PowerShell)
Install dependencies:

bash
pip install -r requirements.txt
Configure your LLM credentials:

Copy .env.example to .env.

Fill in your API key and choose the model.

Example for Google Gemini:

text
GOOGLE_API_KEY=your-google-api-key
GOOGLE_MODEL=gemini-pro-latest
Any LangChain‑compatible model (OpenAI, DeepSeek, etc.) can be used by adjusting the LLM initialization in the scripts.

🚀 Running the Experiment
Zero‑Shot
PetClinic only (default):

bash
python main.py
Bookstore only:

bash
python main.py --system bookstore
Both systems sequentially:

bash
python main.py --all
Few‑Shot
The Few‑Shot scripts inject an example decomposition from the other system (e.g., Bookstore example when testing PetClinic).

PetClinic only:

bash
python main_fewshot.py
Bookstore only:

bash
python main_fewshot.py --system bookstore
Both systems:

bash
python main_fewshot.py --all
Results are saved under result/<system>/few-shot/run_<timestamp>/ to keep them separated from Zero‑Shot runs.

📊 Results Summary
Method	Services (F1)	Interactions (F1)
Zero‑Shot (original paper, GPT‑4)	0.79	0.64
Few‑Shot (original paper, GPT‑4)	0.97	0.86
Our Agent A – Zero‑Shot (best)	0.98	0.88
Our Agent A – Few‑Shot (mean, N=5)	0.95	0.74
Our Consolidator – Few‑Shot (best)	1.00	0.88
The multi‑agent pipeline matches or exceeds the state‑of‑the‑art in its best executions. The asymmetric consolidation prevents the validator from discarding correct interactions produced by the DDD agent. The main remaining challenge is the variability of the Gemini model on the interactions task, which affects the average but not the peak performance.

Detailed execution logs and statistical analysis are available in the project documentation.

📋 Requirements
Python 3.10+

CrewAI

LangChain

A compatible LLM provider (Google Gemini, OpenAI, or DeepSeek)

An .env file with the appropriate API key

📝 License
This project is part of ongoing academic research. Feel free to use it for non‑commercial purposes. For other uses, please contact the authors.

📚 Reference
Pereira, J.R.A. et al. Toward Generating Microservice Architectures from Textual Requirements with Large Language Models. SBCARS 2025.

Our replication and extension is being prepared for submission to ISE 2026.

text

Este `README.md` agora reflete com precisão o escopo completo do projeto, os dois modos de operação (Zero‑Shot e Few‑Shot), a consolidação assimétrica, os resultados obtidos e a estrutura de diretórios atualizada.