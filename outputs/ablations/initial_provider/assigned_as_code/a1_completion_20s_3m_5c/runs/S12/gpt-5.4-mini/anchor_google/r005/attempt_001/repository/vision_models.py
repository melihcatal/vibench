def _first_text(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "description", "name", "label"):
            if key in value and value[key]:
                return str(value[key])
    return str(value)


def normalize_items(items, text_keys=("name", "text", "description"), score_keys=("confidence", "score", "probability")):
    normalized = []
    for item in items or []:
        text = None
        for key in text_keys:
            if isinstance(item, dict) and item.get(key):
                text = str(item[key])
                break
        if text is None:
            text = _first_text(item)
        score = None
        for key in score_keys:
            if isinstance(item, dict) and item.get(key) is not None:
                score = float(item[key])
                break
        entry = {"text": text}
        if score is not None:
            entry["score"] = score
        normalized.append(entry)
    return normalized


def image_bytes_from_payload(payload):
    if isinstance(payload, dict):
        return payload["image_bytes"]
    return payload
