# GenAI-Contract-Risk-Analyzer
This project demonstrates how Generative AI can assist legal and procurement teams by automatically reviewing contract text, identifying risk factors, missing clauses, and suggesting negotiation improvements — laying the foundation for future agent-based automation.

## Run locally (Windows)

### Prerequisites
- Python 3.14+
- Git

### Setup
```powershell
cd "C:\Users\Dell\OneDrive\Documents\GitHub\GenAI-Contract-Risk-Analyzer"
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt

## Working model with Data Science (DS ↔ Engineering)
This repo is structured so Data Science can iterate on modeling without changing the Streamlit UI.

**Interface contract**
- The UI calls a single adapter (`src/model_adapter.py`) that returns a strict schema (`src/schemas.py`).

**Adapter boundary**
- The UI calls a single adapter function: `src/model_adapter.py::analyze_contract()`
- The adapter returns a strict schema: `src/schemas.py::AnalysisResult`

**Ownership (RACI)**
- DS owns: feature/label definitions, scoring logic, thresholds, offline evaluation, model/prompt versions
- Eng/Product owns: UI, orchestration, schema validation, logging/auditability, configuration, deployment readiness

**Contracts**
- Data Contract: `docs/data_contract.md`
- Modeling Contract: `docs/modeling_contract.md`

**Auditability**
- Output includes versions (`model_version`, `ruleset_version`, `prompt_version`) and an audit log.