# Multiagent Microservice Architecture Generation

A multi‑agent framework that generates microservice‑oriented architectures directly from textual requirements using Large Language Models. The pipeline — built with [CrewAI](https://crewai.com) and [LangChain](https://langchain.com) — employs two architect agents (DDD‑based and event‑driven) and a validator agent to produce, compare, and consolidate architectural decompositions. The approach is evaluated on the **Spring PetClinic** and **Bookstore** systems, replicating and extending the study *“Toward Generating Microservice Architectures from Textual Requirements with LLMs”*.

---

## 🧠 How It Works

1. **Agent 1 – Software Architect** proposes a decomposition based on Domain‑Driven Design.
2. **Agent 2 – Alternative Architect** proposes a different decomposition focusing on event‑driven communication, API Gateway patterns, and scalability.
3. **Agent 3 – Architecture Validator** receives both proposals, compares them, explains the differences, and produces a consolidated architecture.

All agents receive the same textual requirements and output a CSV with services, responsibilities, and inter‑service communication. The generated architectures are automatically compared against reference architectures (ground truth) using **Precision**, **Recall**, and **F1‑Score**, both for services (RQ1) and interactions (RQ2).

---

## 📁 Repository Structure
├── main.py # Main orchestration script
├── agentes/
│ ├── agent1_architect_a.py # DDD Architect agent
│ ├── agent2_architect_b.py # Alternative Architect agent
│ ├── agent3_validator.py # Validator / consolidation agent
│ └── init.py
├── result/ # Output files (one folder per run)
│ └── <system>/
│ └── run_<timestamp>/
│ ├── proposta_a.csv
│ ├── proposta_b.csv
│ ├── consolidada.csv
│ ├── metricas_servicos.csv
│ ├── metricas_interacoes.csv
│ └── sumario.json
├── .env.example # Template for environment variables
├── requirements.txt # Python dependencies
├── historico_resultados_petclinic.md # Detailed experiment history
├── contexto_e_proximos_passos.md # Project context and next steps
└── README.md

text

---

## ⚙️ Setup

1. **Clone the repository** and navigate to the project folder.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate.bat     # Windows (cmd)
   .\venv\Scripts\Activate.ps1   # Windows (PowerShell)
Install dependencies:

bash
pip install -r requirements.txt
Configure your LLM credentials:

Copy .env.example to .env.

Fill in your API key and choose the model.

Example for Google Gemini (free tier):

text
GOOGLE_API_KEY=your-google-api-key
GOOGLE_MODEL=gemini-2.0-flash
You can also use OpenAI or DeepSeek by adjusting the LLM initialisation in main.py (CrewAI accepts any LangChain‑compatible model).

🚀 Running the Experiment
PetClinic only (default):

bash
python main.py
Bookstore only:

bash
python main.py --system bookstore
Both systems sequentially:

bash
python main.py --all
Each run creates a timestamped folder inside result/<system>/ containing the generated CSVs and evaluation metrics.

📊 Results (PetClinic – Services)
Method	Precision	Recall	F1‑Score
Zero‑Shot (GPT‑4) – original paper	≈ 0.79	≈ 0.79	≈ 0.79
Few‑Shot (GPT‑4) – original paper	≈ 0.93	≈ 1.00	≈ 0.97
Multi‑Agent (Gemini) – best run	0.88	1.00	0.93
The multi‑agent approach surpasses Zero‑Shot and approaches Few‑Shot without using any example, relying only on the collaboration between architect agents and the validator.

A complete execution history, including problems encountered and fixes applied, is available in historico_resultados_petclinic.md.

📋 Requirements
Python 3.10+

CrewAI

LangChain

A compatible LLM provider (Google Gemini, OpenAI, or DeepSeek)

An .env file with the appropriate API key

🔜 Next Steps (from contexto_e_proximos_passos.md)
Run the experiment for Bookstore (services + interactions)

Execute 5 runs per system and report mean ± standard deviation

Obtain Zero‑Shot and Few‑Shot baselines on the same LLM

Complete the Bookstore interaction reference from .dot files

Generate final comparison tables for the paper

📝 License
This project is part of ongoing academic research. Feel free to use it for non‑commercial purposes. For other uses, please contact the authors.

📚 Reference
Pereira, J.R.A. et al. Toward Generating Microservice Architectures from Textual Requirements with Large Language Models. SBCARS 2025.

Our replication and extension is being prepared for submission to ISE 2026.

text

Esse README está alinhado com o que discutimos e pode ser complementado conforme os experimentos avançarem (ex.: resultados do Bookstore, tabelas de interações).