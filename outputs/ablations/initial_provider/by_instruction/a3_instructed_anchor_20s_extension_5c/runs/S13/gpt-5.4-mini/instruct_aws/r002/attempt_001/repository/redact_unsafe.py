from safety_client import summarize_comprehend_moderation
from safety_models import normalize_text


def redact_unsafe(text):
    content = normalize_text(text)
    decision = summarize_comprehend_moderation(content)
    if decision.allow:
        return {"text": content, "redacted": False, "provider": decision.provider}
    return {"text": "[REDACTED]", "redacted": True, "provider": decision.provider, "categories": decision.categories}
