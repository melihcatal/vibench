from safety_client import SafetyClient
from safety_models import SafetyDecision, SafetyTextRequest, normalize_text


def redact_unsafe(request: SafetyTextRequest) -> SafetyDecision:
    client = SafetyClient()
    text = normalize_text(request.text)
    result = client.analyze_text(text, categories=request.categories)
    spans = result.get("unsafeSpans", []) if isinstance(result, dict) else []
    redacted = text
    for span in sorted(spans, key=lambda x: x.get("offset", 0), reverse=True):
        offset = span.get("offset", 0)
        length = span.get("length", 0)
        redacted = redacted[:offset] + "[REDACTED]" + redacted[offset + length :]
    return SafetyDecision(
        allowed=not spans,
        score=float(bool(spans)),
        categories={},
        reasons=["unsafe_spans"],
        redacted_text=redacted,
    )
