def normalize_image_payload(payload):
    if payload is None:
        return {"image_bytes": b""}
    if isinstance(payload, dict) and "image_bytes" in payload:
        return payload
    return {"image_bytes": payload}


def normalize_text_result(items):
    return {"text": list(items or [])}
