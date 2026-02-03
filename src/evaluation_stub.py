from __future__ import annotations
from pathlib import Path

from .model_adapter import analyze_contract


SAMPLES_DIR = Path("sample_data")


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.txt"))
    if not samples:
        print("No sample contracts found in sample_data/. Add .txt files to run evaluation.")
        return

    scores = []
    for fp in samples:
        contract_text = fp.read_text(encoding="utf-8", errors="ignore")
        result = analyze_contract(contract_text=contract_text, title=fp.stem, source_type="sample_data")

        score = result.summary.overall_risk_score
        level = result.summary.risk_level
        findings_count = len(result.findings)

        scores.append(score)
        print(f"{fp.name}: score={score}, level={level}, findings={findings_count}")

    if scores:
        print("\nSummary")
        print(f"count={len(scores)}  min={min(scores)}  max={max(scores)}  avg={sum(scores)/len(scores):.2f}")


if __name__ == "__main__":
    main()