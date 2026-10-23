from safety_client import get_client, model_name
from safety_models import normalize_text


def redact_unsafe(text: str) -> str:
    client = get_client()
    response = client.moderations.create(
        model=model_name("omni-moderation-latest"), input=normalize_text(text)
    )
    result = response.results[0]
    if not getattr(result, "flagged", False):
        return normalize_text(text)
    redacted = normalize_text(text)
    for category, flagged in dict(getattr(result, "categories", {}) or {}).items():
        if flagged and category:
            redacted = redacted.replace(category, "[REDACTED]")
    return redacted
