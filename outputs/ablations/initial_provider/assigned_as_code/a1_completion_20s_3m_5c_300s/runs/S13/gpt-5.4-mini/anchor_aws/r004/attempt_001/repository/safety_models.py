def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    return payload or {}


def normalize_texts(payload):
    payload = payload or {}
    texts = payload.get("texts")
    if texts is None and "items" in payload:
        texts = payload["items"]
    return [item if isinstance(item, str) else item.get("text", "") for item in (texts or [])]


def normalize_categories(categories):
    return {str(k).lower(): float(v) for k, v in (categories or {}).items()}
