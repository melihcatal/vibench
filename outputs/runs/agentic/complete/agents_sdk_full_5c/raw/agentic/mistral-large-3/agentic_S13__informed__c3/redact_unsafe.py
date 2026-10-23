from typing import List
from safety_client import get_watsonx_client
from safety_models import TextRedactionResponse, RedactionSpan, SafetyCategory


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> TextRedactionResponse:
    """
    Redact unsafe spans from text using WatsonX.ai guardrails.
    Returns redacted text and spans.
    """
    client = get_watsonx_client()
    raw_response = client.analyze_text(text)

    # Example redaction logic (adjust based on actual response structure)
    spans: List[RedactionSpan] = []
    redacted_text = text
    offset = 0

    if "results" in raw_response:
        for category in SafetyCategory:
            if raw_response["results"].get(category.value, 0.0) > 0.5:
                # Simulate span detection (replace with actual span logic)
                start = text.find(category.value)
                if start != -1:
                    end = start + len(category.value)
                    spans.append({
                        "start": start,
                        "end": end,
                        "category": category,
                        "replacement": replacement
                    })
                    redacted_text = (
                        redacted_text[:start + offset] +
                        replacement +
                        redacted_text[end + offset:]
                    )
                    offset += len(replacement) - (end - start)

    return TextRedactionResponse(
        raw_response=raw_response,
        redacted_text=redacted_text,
        spans=spans
    )