from safety_client import PerspectiveAPIClient
from safety_models import RedactionResult, RedactionSpan


def redact_unsafe(text: str, threshold: float = 0.8) -> RedactionResult:
    client = PerspectiveAPIClient()
    response = client.analyze(text)

    is_unsafe = False
    for attribute, data in response.get("attributeScores", {}).items():
        score = data["summaryScore"]["value"]
        if score > threshold:
            is_unsafe = True
            break

    if is_unsafe:
        redacted_text = "[REDACTED]"
        redaction_spans = [
            RedactionSpan(
                begin=0, end=len(text), original_text=text, redacted_text=redacted_text
            )
        ]
    else:
        redacted_text = text
        redaction_spans = []

    return RedactionResult(
        original_text=text, redacted_text=redacted_text, redaction_spans=redaction_spans
    )
