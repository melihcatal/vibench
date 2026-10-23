from safety_models import build_decision


def safety_threshold(payload, config=None):
    config = config or {}
    thresholds = config.get("thresholds") or {}
    scores = payload.get("scores") or {}
    decisions = {}
    allow = True
    for category, score in scores.items():
        threshold = thresholds.get(category, 0.5)
        decision = build_decision(score, threshold)
        decisions[category] = decision
        allow = allow and decision["allow"]
    return {"allow": allow, "decisions": decisions}
