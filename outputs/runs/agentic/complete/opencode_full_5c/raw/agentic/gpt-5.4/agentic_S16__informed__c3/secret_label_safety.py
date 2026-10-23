from __future__ import annotations

from security_client import perspective_analyze
from security_models import LabelSafetyReport, normalize_label_safety


def secret_label_safety(text: str, threshold: float = 0.7) -> dict:
    response = perspective_analyze(text)
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in response.get("attributeScores", {}).items()
    }
    flagged = [name for name, score in scores.items() if score >= threshold]
    report = LabelSafetyReport(
        text=text,
        unsafe=bool(flagged),
        risk_scores=scores,
        flagged_categories=flagged,
    )
    return normalize_label_safety(report)
