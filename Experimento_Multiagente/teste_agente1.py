import os
from dotenv import load_dotenv

from crewai import LLM
from agentes.agent1 import criar_agente1


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise Exception("GOOGLE_API_KEY não encontrada")


llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=api_key,
    temperature=0.2
)


agente1 = criar_agente1(llm)


print("\n===== AGENTE 1 =====")
print(agente1.role)
print(agente1.goal)
print("====================")


resposta = agente1.execute_task(
    "Analise a arquitetura do Spring Petclinic e liste seus principais serviços."
)


print("\n===== RESPOSTA =====")
print(resposta)