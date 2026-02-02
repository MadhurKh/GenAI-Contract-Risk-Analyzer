from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Severity = Literal["High", "Medium", "Low"]
RiskLevel = Literal["High", "Medium", "Low"]

class Evidence(BaseModel):
    clause_ref: str
    snippet: str

class Finding(BaseModel):
    finding_id: str
    category: str
    risk_statement: str
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[Evidence]
    recommendation: str
    proposed_redline: Optional[str] = None

class Summary(BaseModel):
    overall_risk_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    top_risks: List[dict]

class AuditEvent(BaseModel):
    ts: str
    event: str

class ContractMeta(BaseModel):
    title: str
    source_type: str
    text_length: int

class AnalysisResult(BaseModel):
    run_id: str
    contract: ContractMeta
    summary: Summary
    findings: List[Finding]
    audit: List[AuditEvent]