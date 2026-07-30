"""
Agente 4: Domain-Driven Refiner (Few‑Shot)
Revisa uma proposta de arquitetura e remove SOMENTE comunicações que
NÃO podem ser diretamente justificadas pelos requisitos originais.
NUNCA remove um serviço que é claramente mencionado nas user stories.
"""

from crewai import Agent, Task


def criar_agente4(llm):
    agente = Agent(
        role="Domain-Driven Refiner",
        goal="""
        Revisar uma arquitetura de microsserviços gerada por outro agente e 
        eliminar SOMENTE comunicações entre serviços que não sejam EXPLICITAMENTE 
        exigidas pelas histórias de usuário (user stories) fornecidas.
        
        Regras:
        1. NUNCA remova um serviço que corresponda a uma seção dos requisitos 
           (ex.: "Manage Deliveries" sempre exige um "Delivery Service").
        2. Remova uma comunicação (um destino no campo 'Communicates With') apenas 
           se NENHUMA história de usuário exigir troca de dados ou ação entre 
           aqueles dois serviços.
        3. NUNCA adicione novos serviços ou comunicações.
        4. Mantenha todas as responsabilidades exatamente como estão no CSV original.
        """,
        backstory="""
        Você é um revisor arquitetural extremamente preciso. Sua função é apenas 
        podar conexões desnecessárias entre serviços, sem jamais remover um serviço 
        que tenha uma história de usuário dedicada. Você trabalha como um filtro 
        conservador: só elimina o que for indubitavelmente sem suporte.
        """,
        llm=llm,
        verbose=True,
        memory=False,
    )
    return agente


def criar_task_refinamento(agente):
    task = Task(
        description="""
        You are given an ORIGINAL ARCHITECTURE (CSV) and the SYSTEM REQUIREMENTS 
        (user stories) that motivated it.

        Your job: output a CLEANED VERSION of the CSV.
        - NEVER delete a service that matches a requirement section title.
        - Keep ALL communications between domain services (services that directly
          implement a user story section, e.g., "Client Service", "Visit Service").
          DO NOT remove any communication between two domain services.
        - ONLY remove a communication if it involves an infrastructure service
          AND that specific interaction is not implied by the infrastructure's
          core function described in the requirements. For example, API Gateway
          routes to all business services, Config Server serves configuration to
          all services, Admin Server monitors all services – these general
          interactions should be KEPT. Remove only interactions that are clearly
          unjustified (e.g., Gateway talking to an external payment provider not
          mentioned in requirements).
        - Keep all responsibilities identical to the original.

        IMPORTANT: Every output line MUST have exactly three columns, even if the 
        last one is empty. Never leave a line incomplete.

        ORIGINAL ARCHITECTURE:
        {original_architecture}

        SYSTEM REQUIREMENTS (user stories):
        {requirements}

        OUTPUT FORMAT (CSV exactly, no extra text):
        Microservice,Responsibilities,Communicates With
        Service Name,resp1;resp2,ServiceX;ServiceY
        """,
        expected_output="CSV with infrastructure-only communications removed, all domain communications preserved",
        agent=agente,
    )
    return task