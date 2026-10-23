from safety_client import get_openai_client, moderation_model, parse_moderation_result
from safety_models import TextSafetyRequest, normalize_spans


def redact_unsafe(value):
    req = TextSafetyRequest.from_input(value)
    client = get_openai_client()
    result = client.moderations.create(model=moderation_model(), input=req.text)
    parsed = parse_moderation_result(result)
    item = parsed.get("results", [{}])[0]
    spans = normalize_spans(item.get("content_filter_results", {}).get("spans", []))
    redacted = req.text
    for span in sorted(spans, key=lambda s: s["start"], reverse=True):
        redacted = redacted[: span["start"]] + "[REDACTED]" + redacted[span["end"] :]
    return {
        "text": req.text,
        "redacted_text": redacted,
        "spans": spans,
        "flagged": bool(item.get("flagged")),
        "raw": parsed,
    }
