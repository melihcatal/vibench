from typing import Any, Dict, List

from translation_client import analyze_text_with_perspective


def unsafe_copy_check(text: str, language: str | None = None) -> Dict[str, Any]:
    payload = analyze_text_with_perspective(
        text, languages=[language] if language else None
    )
    scores = payload.get("attributeScores", {})
    extracted = {
        name.lower(): details.get("summaryScore", {}).get("value", 0.0)
        for name, details in scores.items()
    }
    max_score = max(extracted.values(), default=0.0)
    return {
        "provider": "google_perspective_api",
        "unsafe": max_score >= 0.7,
        "scores": extracted,
        "flagged_attributes": [
            name for name, value in extracted.items() if value >= 0.7
        ],
    }
