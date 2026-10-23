from safety_models import RedactionResult


def redact_unsafe(text: str, unsafe_spans):
    redacted = text
    spans = []
    for start, end in sorted(unsafe_spans, reverse=True):
        redacted = redacted[:start] + "[REDACTED]" + redacted[end:]
        spans.append({"start": start, "end": end})
    return RedactionResult(text=redacted, spans=list(reversed(spans)))
