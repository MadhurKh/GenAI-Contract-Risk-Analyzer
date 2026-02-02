from __future__ import annotations
from datetime import datetime, timezone
import random, string

from .schemas import AnalysisResult, ContractMeta, Summary, Finding, Evidence, AuditEvent

def _run_id() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    return f"{ts}_{suffix}"

def analyze_contract(contract_text: str, title: str, source_type: str) -> AnalysisResult:
    """
    Adapter boundary.
    Later you replace internals with your actual prompt pipeline / RAG
    without changing the Streamlit UI code.
    """
    rid = _run_id()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    findings = [
        Finding(
            finding_id="R-001",
            category="Liability",
            risk_statement="Liability appears uncapped and includes consequential damages.",
            severity="High",
            confidence=0.78,
            evidence=[Evidence(clause_ref="Section 9.2", snippet="...liable for all damages including consequential...")],
            recommendation="Cap liability to 12 months of fees and exclude consequential damages.",
            proposed_redline="Total liability shall not exceed fees paid in the preceding 12 months..."
        ),
        Finding(
            finding_id="R-002",
            category="Termination",
            risk_statement="Termination for convenience may allow exit without cure period.",
            severity="Medium",
            confidence=0.70,
            evidence=[Evidence(clause_ref="Section 12.1", snippet="Either party may terminate at any time upon notice...")],
            recommendation="Add cure period and limit termination for convenience."
        ),
    ]

    score = 72
    return AnalysisResult(
        run_id=rid,
        contract=ContractMeta(title=title, source_type=source_type, text_length=len(contract_text)),
        summary=Summary(
            overall_risk_score=score,
            risk_level="High",
            top_risks=[
                {"category": "Liability", "title": "Uncapped liability / consequential damages"},
                {"category": "Termination", "title": "Termination for convenience without protections"},
            ],
        ),
        findings=findings,
        audit=[
            AuditEvent(ts=now, event="UPLOAD_RECEIVED"),
            AuditEvent(ts=now, event="ANALYSIS_COMPLETED"),
        ],
    )