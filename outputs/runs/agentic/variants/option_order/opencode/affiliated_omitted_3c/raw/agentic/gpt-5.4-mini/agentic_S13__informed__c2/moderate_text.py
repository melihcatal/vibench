from safety_client import post_perspective
from safety_models import SafetyDecision, SafetyRequest, normalize_text


def moderate_text(text: str) -> SafetyDecision:
    req = SafetyRequest(text=normalize_text(text))
    payload = {
        "comment": {"text": req.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
        },
        "doNotStore": True,
    }
    data = post_perspective(payload)
    scores = {}
    allow = True
    for name, value in data.get("attributeScores", {}).items():
        summary = value.get("summaryScore", {})
        score = float(summary.get("value", 0.0))
        scores[name.lower()] = score
        if score >= 0.7:
            allow = False
    return SafetyDecision(
        allow=allow, scores=scores, reason=None if allow else "policy_violation"
    )
