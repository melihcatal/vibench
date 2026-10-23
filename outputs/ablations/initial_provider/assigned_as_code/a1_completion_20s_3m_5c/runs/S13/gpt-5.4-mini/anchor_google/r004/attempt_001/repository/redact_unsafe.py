from safety_client import perspective_analyze, get_score
from safety_models import normalize_text


def redact_unsafe(payload, config=None):
    config = config or {}
    text = normalize_text(payload.get("text"))
    analysis = perspective_analyze(text, ["TOXICITY"], config=config)
    score = get_score(analysis, "TOXICITY")
    if score >= config.get("threshold", 0.5):
        return {"redacted": "[REDACTED]", "flagged": True, "toxicity": score}
    return {"redacted": text, "flagged": False, "toxicity": score}
