"""
Agente 3: Validator Agent (Validador) – Few‑Shot (idêntico ao original)
Responsável por comparar duas propostas de arquitetura e gerar versão consolidada

Baseado no notebook multiagent_architecture_generation.ipynb - Fase 4
"""

from crewai import Agent, Task


def criar_agente3(llm):
    agente = Agent(
        role="Architecture Validator",
        goal="""
        Comparar duas propostas de arquitetura de microsserviços e gerar uma versão consolidada.
        
        Você deve:
        1. Analisar ambas as propostas (Architect A e Architect B)
        2. Identificar serviços comuns entre elas
        3. Identificar serviços únicos de cada proposta
        4. Consolidar em uma arquitetura final que combine o melhor de ambas
        5. Explicar as decisões de consolidação
        """,
        backstory="""
        Você é um arquiteto líder com vasta experiência em revisão de designs.
        
        Sua especialidade:
        - Revisão e validação de arquiteturas de software
        - Identificação de overlaps e gaps em propostas
        - Tomada de decisão baseada em trade-offs
        - Comunicação clara de decisões arquiteturais
        
        Você consegue enxergar o melhor de diferentes abordagens
        e combiná-las em uma solução coesa e bem fundamentada.
        """,
        llm=llm,
        verbose=True,
        memory=True,
    )
    return agente


def criar_task_consolidacao(agente):
    task = Task(
        description="""
        Compare the two architecture proposals below and generate a consolidated version.

        IMPORTANT RULES FOR CONSOLIDATION:
        - Prefer services that appear in BOTH proposals (they are highly likely to be correct).
        - If a service appears in only one proposal, include it ONLY if it is clearly grounded in the requirements.
        - Do NOT add new services that were not in either proposal.
        - Do NOT add infrastructure services (gateway, config, discovery, admin) unless they are present in BOTH proposals.
        - Choose the simplest, most generic service name when merging similar services.
        - Aim to maximize precision: only include services that are necessary to cover the requirements.
        - If the intersection of services between both proposals contains fewer than 3 services,
          discard Architecture B and adopt Architecture A entirely.

        ARCHITECTURE A (Traditional DDD approach):
        {architecture_a}

        ARCHITECTURE B (Alternative approach):
        {architecture_b}

        Your output MUST be in this format:
        === CONSOLIDATED ARCHITECTURE ===
        Microservice,Responsibilities,Communicates With,Source
        Service Name,resp1;resp2,ServiceX;ServiceY,A+B

        === DECISIONS ===
        - Service X: Kept from both proposals because...
        - Service Y: Merged from A's name and B's responsibilities because...
        - Service Z: Added from B only because...

        Rules:
        - Include a 'Source' column indicating where each service came from (A, B, or A+B)
        - Explain key decisions
        - Be specific about why certain services were kept, merged, or discarded
        """,
        expected_output="Consolidated architecture with decisions explained",
        agent=agente,
    )
    return task