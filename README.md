# GenAI Contract Risk Analyzer (Portfolio Demo)

This project demonstrates how Generative AI can assist legal/procurement teams by reviewing contract text, identifying risk factors and missing protections, and producing **enterprise-style outputs**:
- Structured risk register (findings + evidence)
- Extracted feature set (DS handshake layer)
- Explainable scoring breakdown (severity weights + confidence)
- Audit log + exportable JSON

> Current implementation is rule-based for portability and transparency, but the repo is structured so a Data Science team can replace internals with an LLM/RAG/model pipeline **without changing the UI**.

---

## Quick Start (Windows)

### Prerequisites
- Python 3.14+
- Git

### Setup + Run
```powershell
cd "C:\Users\Dell\OneDrive\Documents\GitHub\GenAI-Contract-Risk-Analyzer"
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m streamlit run streamlit_ui/dashboard.py