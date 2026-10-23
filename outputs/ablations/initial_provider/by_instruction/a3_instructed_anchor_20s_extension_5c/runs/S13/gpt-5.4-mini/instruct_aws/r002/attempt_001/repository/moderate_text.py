from safety_client import summarize_comprehend_moderation
from safety_models import normalize_text


def moderate_text(text):
    content = normalize_text(text)
    if not content:
        return {"allow": True, "reason": "empty", "provider": "aws"}
    decision = summarize_comprehend_moderation(content)
    return {"allow": decision.allow, "categories": decision.categories, "provider": decision.provider, "raw": decision.raw}
