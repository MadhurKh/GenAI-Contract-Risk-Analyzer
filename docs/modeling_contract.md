# Modeling Contract (Data Science ↔ Engineering)

## 1) Objective
The system analyzes contract text and produces:
- A normalized **Risk Score (0–100)**
- A categorical **Risk Level** (Low/Medium/High)
- A **Risk Register** (list of findings with evidence + rationale)
- An **Audit Log** of what rules/prompts/components were used

This is designed so DS can improve modeling without changing UI.

---

## 2) Inputs (from UI → Model)
Primary input:
- `contract_text: str`

Optional metadata:
- `contract_title: str`
- `contract_type: str` (MSA/SOW/NDA/etc.)
- `jurisdiction: str`
- `party_role: str` (customer/vendor)

Schema source of truth: `src/schemas.py`

---

## 3) Outputs (Model → UI)
The model must return a structured object matching `RiskAnalysisResult`:

- `overall_risk_score: int (0..100)`
- `risk_level: str (Low/Medium/High)`
- `findings: List[RiskFinding]`
- `evidence: List[EvidenceItem]`
- `audit_log: List[AuditEvent]`
- `meta: { model_version, ruleset_version, prompt_version }`

Schema source of truth: `src/schemas.py`

---

## 4) Thresholding / Calibration (DS-owned)
Mapping from score → level is DS-owned and must be configurable, e.g.
- 0–34 = Low
- 35–69 = Medium
- 70–100 = High

Change mechanism:
- constants/config file OR environment variable OR model config JSON

---

## 5) Evaluation Hooks (DS-owned)
Offline evaluation can be run using:
- a labeled dataset of clauses and risks
- scenario-based tests

Suggested metrics:
- Precision/Recall for each risk category
- Calibration curves (score vs observed risk)
- False positive analysis for high-risk labels

---

## 6) Versioning (Joint)
Every result should include:
- `model_version` (DS)
- `prompt_version` (DS/Product)
- `ruleset_version` (Eng/Product)

Purpose: auditability + reproducibility.

---

## 7) Deployment Notes (Engineering-owned)
- Output must be deterministic schema-wise (no missing keys)
- Errors must be caught and logged (no UI crashes)
- PII handling guidance should be in README