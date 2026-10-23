from typing import Dict, List, Optional
from safety_client import PerspectiveClient
from safety_models import RedactionResult


def redact_unsafe(
    text: str, threshold: float = 0.7, attributes: Optional[List[str]] = None
) -> RedactionResult:
    """Flag or redact unsafe spans from text using Perspective API."""
    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    client = PerspectiveClient()
    raw_response = client.moderate_text(text)
    spans = []

    for attr in attributes:
        if attr in raw_response.get("attributeScores", {}):
            score = raw_response["attributeScores"][attr]["summaryScore"]["value"]
            if score >= threshold:
                spans.append(
                    {"start": 0, "end": len(text), "attribute": attr, "score": score}
                )

    redacted_text = text
    for span in sorted(spans, key=lambda x: x["start"], reverse=True):
        start, end = span["start"], span["end"]
        redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]

    return RedactionResult(
        original_text=text, redacted_text=redacted_text, unsafe_spans=spans
    )
