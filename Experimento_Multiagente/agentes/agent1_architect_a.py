"""
Agente 1: Software Architect (Arquiteto A)
Abordagem tradicional DDD (Domain Driven Design)
Foco: Decomposição baseada em bounded contexts

Baseado no notebook multiagent_architecture_generation.ipynb - Fase 2
"""

from crewai import Agent, Task


def criar_agente1(llm):
    """
    Cria o Agente 1 - Software Architect (Arquiteto Tradicional)
    
    Especialização: Microsserviços, Domain Driven Design (DDD),
    Decomposição baseada em responsabilidades
    
    Args:
        llm: Modelo de linguagem configurado (Google Gemini via CrewAI LLM)
    
    Returns:
        Agent: Agente CrewAI configurado
    """
    agente = Agent(
        role="Software Architect",
        goal="""
        Propor uma arquitetura de microsserviços baseada em requisitos textuais.
        
        Para cada microsserviço, você deve:
        1. Identificar um nome descritivo baseado em responsabilidades de negócio
        2. Listar as responsabilidades principais
        3. Especificar quais outros serviços ele se comunica

        IMPORTANTE: Inclua SEMPRE os serviços de infraestrutura mencionados nos requisitos,
        como API Gateway, Service Discovery (Eureka), Config Server e Admin Server,
        além dos serviços de domínio.

        Use princípios de Domain Driven Design (DDD) e bounded contexts.
        """,
        backstory="""
        Você é um arquiteto de software sênior especializado em microsserviços.
        
        Sua experiência inclui:
        - Decomposição de monólitos usando Domain Driven Design
        - Identificação de bounded contexts
        - Design de comunicação entre serviços
        - Análise de responsabilidades de negócio
        
        Você pensa criteriosamente sobre a estrutura de um sistema,
        buscando separação clara de responsabilidades e coesão máxima.
        """,
        llm=llm,
        verbose=True,
        memory=False,
    )
    return agente


def criar_task_arquitetura(agente):
    """
    Cria a Task para gerar arquitetura de microsserviços
    
    Args:
        agente: O agente que executará a task
    
    Returns:
        Task: Task CrewAI configurada
    """
    task = Task(
        description="""
        Analyze the following system requirements and propose a microservices architecture.

        You MUST include ALL services mentioned in the requirements, including infrastructure services
        (API Gateway, Service Discovery, Config Server, Admin Server) and domain services.
        
        Your output MUST be EXACTLY in this CSV format (no markdown, no explanations):
        
        Microservice,Responsibilities,Communicates With
        Service Name,responsibility1;responsibility2;responsibility3,Service1;Service2;Service3
        
        Rules:
        - One row per microservice
        - Separate multiple items with semicolons (;)
        - NO markdown formatting, NO headers, NO extra text
        - List services in a logical order
        - Consider DDD bounded contexts
        - INCLUDE ALL infrastructure services (gateway, discovery, config, admin)
        
        System Requirements:
        {requirements}
        """,
        expected_output="CSV format with microservices, their responsibilities, and communications",
        agent=agente,
    )
    return task