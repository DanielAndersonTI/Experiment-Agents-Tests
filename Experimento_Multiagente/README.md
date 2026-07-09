# MultiAgent Architecture Generation Experiment

## Visão Geral

Este experimento implementa um sistema multiagente usando **CrewAI** e **LangChain** para gerar arquiteturas de microsserviços a partir de requisitos textuais.

### Estrutura dos Agentes

1. **Agente A (Arquiteto)** - Gera primeira proposta de decomposição
2. **Agente B (Arquiteto)** - Gera segunda proposta independente
3. **Agente Validador** - Compara as propostas e gera arquitetura consolidada
4. **Avaliação** - Compara com arquitetura de referência (Precision, Recall, F1)

---

## Estrutura de Diretórios

```
Experimento_Multiagente/
├── notebooks/
│   └── multiagent_architecture_generation.ipynb    ← Notebook principal
├── results/                                        ← Saídas dos agentes
│   ├── agent_a_proposals/
│   ├── agent_b_proposals/
│   ├── validator_consolidations/
│   └── evaluation_metrics/
├── config/                                         ← Configurações
│   └── (futuros arquivos de config)
├── requirements.txt                                ← Dependências
├── .env.example                                    ← Template de variáveis
└── README.md                                       ← Este arquivo
```

---

## Setup Inicial

### 1. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar API Key

```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar sua chave OpenAI
# OPENAI_API_KEY=sk-...your-key...
```

### 4. Validar Ambiente

Abra o notebook `notebooks/multiagent_architecture_generation.ipynb` e execute as células:

- **Célula 1:** Importações
- **Célula 2:** Carregamento do .env
- **Célula 3:** Inicialização do modelo
- **Célula 4:** Teste de conexão

Se todas as células executarem sem erros, o ambiente está pronto ✓

---

## Fase 1: Setup (ATUAL)

✅ **Concluído:**
- Estrutura de pastas criada
- Notebook base com imports e configuração
- requirements.txt com dependências
- .env.example com template

📋 **Validar:**
- Executar teste de conexão no notebook

---

## Fase 2: Definição de Agentes (PRÓXIMA)

Tasks:
- [ ] Definir prompt do Agente A (Arquiteto 1)
- [ ] Definir prompt do Agente B (Arquiteto 2)
- [ ] Definir prompt do Agente Validador
- [ ] Criar instâncias de Agent com CrewAI

---

## Fase 3: Implementação de Tasks

Tasks:
- [ ] Task para Agente A gerar arquitetura
- [ ] Task para Agente B gerar arquitetura
- [ ] Task para Validador comparar e consolidar
- [ ] Output em formato CSV e DOT

---

## Fase 4: Orquestração com Crew

Tasks:
- [ ] Criar Crew com os 3 agentes
- [ ] Definir fluxo de execução (sequencial ou paralelo)
- [ ] Integração com casos de estudo (Bookstore, PetClinic)

---

## Fase 5: Avaliação

Tasks:
- [ ] Implementar parser CSV → grafo
- [ ] Implementar comparador de grafos
- [ ] Calcular Precision, Recall, F1
- [ ] Gerar relatório de comparação

---

## Arquivos de Entrada (Reutilizáveis)

### Requisitos
- `../../../Artefatos_Reproducao/Systems Artifacts/bookstore_requirements.txt`
- `../../../Artefatos_Reproducao/Systems Artifacts/petclinic_requirements.txt`

### Arquitetura de Referência
- `../../../Artefatos_Reproducao/Dot Files/bookstore_ref.dot`
- `../../../Artefatos_Reproducao/Dot Files/petclinic_ref.dot`

### Outputs do Experimento Original
- `../../../Artefatos_Reproducao/LLM Architecture Generation/Results/`

---

## Recursos Úteis

### CrewAI Docs
- [CrewAI Documentation](https://docs.crewai.com/)
- [Agent Configuration](https://docs.crewai.com/agents/)
- [Task Definition](https://docs.crewai.com/tasks/)

### LangChain
- [ChatOpenAI](https://python.langchain.com/docs/integrations/chat/openai/)
- [Messages](https://python.langchain.com/docs/concepts/messages/)

### OpenAI Models
- Documentação: [platform.openai.com/docs](https://platform.openai.com/docs/models)
- Pricing: [openai.com/api/pricing](https://openai.com/api/pricing/)

---

## Notas Importantes

1. **API Key:** Mantenha em segredo. Nunca faça commit do `.env`
2. **Custos:** Monitore uso de tokens. Modelo "o3" tem pricing específico
3. **Rate Limits:** OpenAI tem limites por minuto (ajustáveis na conta)
4. **Reproducibilidade:** Temperature = 0.3 para resultados determinísticos

---

## Status: ✅ READY FOR PHASE 2

O ambiente está pronto para implementação dos agentes na próxima fase.
