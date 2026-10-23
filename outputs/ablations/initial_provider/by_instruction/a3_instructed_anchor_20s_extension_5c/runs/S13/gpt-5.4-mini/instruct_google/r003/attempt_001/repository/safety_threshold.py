from safety_client import score_text


def safety_threshold(text, thresholds, categories=None):
    decision = score_text(text, categories=categories, thresholds=thresholds)
    return {"allowed": decision.allowed, "decision": decision}
