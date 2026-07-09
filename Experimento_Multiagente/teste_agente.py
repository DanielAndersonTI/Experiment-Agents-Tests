import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI


# Carrega variáveis do .env
load_dotenv()


# Verifica API KEY
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise Exception("GOOGLE_API_KEY não encontrada no arquivo .env")

print("✓ API KEY encontrada")


# Configura Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.2
)


# Criando agente simples
agente = Agent(
    role="Analista de Sistemas",
    goal="Analisar arquitetura de software",
    backstory="""
    Você é especialista em engenharia de software
    e arquitetura de sistemas distribuídos.
    """,
    llm=llm,
    verbose=True
)


# Tarefa
tarefa = Task(
    description="""
    Explique em poucas linhas a arquitetura
    de microsserviços do Spring Petclinic.
    """,
    expected_output="""
    Uma explicação técnica contendo:
    - serviços existentes
    - comunicação
    - benefícios
    """,
    agent=agente
)


# Executa
crew = Crew(
    agents=[agente],
    tasks=[tarefa],
    verbose=True
)


resultado = crew.kickoff()

print("\n========== RESULTADO ==========\n")
print(resultado)