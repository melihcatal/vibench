from __future__ import annotations

from typing import Any, Dict

from document_client import analyze_perspective_text


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    result = analyze_perspective_text(text)
    attribute_scores = result.get("attributeScores", {})
    summary = {
        name.lower(): scores.get("summaryScore", {}).get("value", 0.0)
        for name, scores in attribute_scores.items()
    }
    flagged = any(score >= 0.7 for score in summary.values())
    return {
        "provider": "perspective_api",
        "flagged": flagged,
        "scores": summary,
        "raw": result,
    }
