from safety_client import moderate_text_payload, threshold_allow


def safety_threshold(text, thresholds=None):
    payload = moderate_text_payload(text)
    return {
        "allow": threshold_allow(payload["category_scores"], thresholds),
        "category_scores": payload["category_scores"],
    }
