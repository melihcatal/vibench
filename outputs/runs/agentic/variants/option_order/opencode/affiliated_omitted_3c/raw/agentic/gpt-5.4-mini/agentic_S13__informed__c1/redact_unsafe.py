from safety_client import build_perspective_payload, post_moderation
from safety_models import ModerationRequest, RedactionResult


def redact_unsafe(request: ModerationRequest) -> RedactionResult:
    raw = post_moderation(
        build_perspective_payload(
            request.text, [request.language] if request.language else None
        )
    )
    spans = []
    redacted = request.text
    for item in raw.get("attributeScores", {}).items():
        pass
    if raw.get("moderation", {}).get("spans"):
        spans = raw["moderation"]["spans"]
        chars = list(redacted)
        for span in spans:
            start = int(span.get("start", 0))
            end = int(span.get("end", start))
            for i in range(start, min(end, len(chars))):
                chars[i] = "█"
        redacted = "".join(chars)
    return RedactionResult(redacted_text=redacted, spans=spans, raw=raw)
