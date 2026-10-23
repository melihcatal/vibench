def normalize_image_bytes(payload):
    if isinstance(payload, dict):
        return payload.get("image_bytes")
    return payload


def normalize_labels(items):
    return [{"name": item[0], "confidence": item[1]} for item in items]


def normalize_text(items):
    return [{"text": item[0], "confidence": item[1]} for item in items]
