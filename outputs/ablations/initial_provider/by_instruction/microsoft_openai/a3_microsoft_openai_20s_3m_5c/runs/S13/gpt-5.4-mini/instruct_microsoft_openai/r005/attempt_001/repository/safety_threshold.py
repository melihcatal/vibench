from safety_client import moderate_text_openai


def safety_threshold(text: str, thresholds=None):
    decision = moderate_text_openai(text)
    thresholds = thresholds or {}
    for category, score in decision.category_scores.items():
        if score >= float(thresholds.get(category, 1.0)):
            decision.flagged = True
    return decision
