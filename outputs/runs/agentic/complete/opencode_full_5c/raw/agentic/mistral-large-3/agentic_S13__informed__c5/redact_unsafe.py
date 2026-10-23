from typing import Dict, List, Union
from safety_client import WatsonXGuardrailsClient
from safety_models import RedactionResult


def redact_unsafe(text: str) -> RedactionResult:
    """Flag or redact unsafe spans from text using WatsonX Guardrails."""
    client = WatsonXGuardrailsClient()
    result = client.moderate_text(text)

    unsafe_spans = []
    redacted_text = text

    if not result["is_safe"]:
        # Simulate redaction based on categories (WatsonX Guardrails does not provide spans)
        for category, score in result["categories"].items():
            if score >= 0.75:
                unsafe_spans.append(
                    {"start": 0, "end": len(text), "category": category, "score": score}
                )
        redacted_text = "[REDACTED]"

    return RedactionResult(
        redacted_text=redacted_text,
        unsafe_spans=unsafe_spans,
        is_safe=result["is_safe"],
    )
