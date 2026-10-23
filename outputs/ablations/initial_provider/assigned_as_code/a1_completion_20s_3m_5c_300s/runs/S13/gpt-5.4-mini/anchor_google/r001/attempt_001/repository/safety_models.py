def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    return payload


def normalize_texts(payload):
    payload = payload or {}
    texts = payload.get("texts") or payload.get("messages") or []
    return [normalize_text_payload(item)["text"] if isinstance(item, dict) else str(item) for item in texts]


def decision_from_score(score, threshold):
    return {"score": score, "allow": score < threshold, "threshold": threshold}
