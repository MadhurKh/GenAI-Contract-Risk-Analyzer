# 2–3 Minute Demo Script — GenAI Contract Risk Analyzer (Citi-ready)

## Goal (10 seconds)
Demonstrate an enterprise-style GenAI application that:
- Converts unstructured contract text into structured risk outputs
- Produces audit-friendly artifacts (risk register, evidence, audit log, data contract)
- Uses a DS-friendly interface contract so modeling can evolve without UI rewrites

---

## Setup (10 seconds)
1. Start the app:
   - `py -m streamlit run streamlit_ui/dashboard.py`
2. Open: `http://localhost:8501`

---

## Step 1 — Input (15 seconds)
- Paste a contract excerpt (or use a sample contract).
- Optional: choose contract type / jurisdiction if the UI has it.

**What to say:**
“This system accepts raw contract text, the same format legal and procurement teams receive in reality.”

---

## Step 2 — Output (45 seconds)
Point to the top summary:
- **Overall Risk Score** (0–100)
- **Risk Level** (Low / Medium / High)
- **Findings count**

Open the **Risk Register** section:
- Show each finding: category, severity, recommendation/mitigation

**What to say:**
“The output is structured, not a chat response. It’s a risk register that can be used downstream by legal/procurement teams.”

---

## Step 3 — Evidence (30 seconds)
Open the **Evidence** tab/section:
- Show clause snippets mapped to each finding

**What to say:**
“Every risk is backed by traceable evidence. This avoids ‘black box’ outputs and makes it reviewable.”

---

## Step 4 — Auditability (30 seconds)
Open **Audit Log**:
- Show steps, components invoked, versions

**What to say:**
“This is designed for enterprise governance: audit log + version metadata for reproducibility and control.”

---

## Step 5 — Data Contract (20 seconds)
Open **Data Contract**:
- Show the input/output schema expectations

**What to say:**
“This is where engineering and data science align. Schemas are source-of-truth, enabling consistent integration and testing.”

---

## How I work with Data Science (40 seconds) — Directly addressing the concern
**What to say (use this verbatim):**
“I collaborate with data science using explicit contracts and stable interfaces:
- The UI calls a single adapter layer (`src/model_adapter.py`) and expects a strict schema (`src/schemas.py`).
- DS can swap the scoring logic (rules/ML/LLM) without changing UI code.
- We agree on thresholds/calibration and evaluation hooks in `docs/modeling_contract.md`.
This is the same pattern used in production teams to iterate on models safely.”

---

## Close (10 seconds)
**What to say:**
“Today this demonstrates an end-to-end working product demo with enterprise outputs. Next steps are adding a labeled dataset and evaluation metrics to operationalize model iteration and drift monitoring.”

---

## Optional Q&A prompts (if asked)
**Q: What would you do next to productionize?**
- Add offline evaluation harness + metrics (precision/recall, calibration)
- Add CI tests for schema stability
- Containerize + deploy with secrets management
- Add PII guidance + redaction
- Add monitoring for drift / usage

**Q: Where does data modeling fit here?**
- Define a canonical schema for findings/evidence/audit events
- Version schemas
- Maintain backward compatibility for downstream consumers