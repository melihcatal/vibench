def normalize_image_payload(payload):
    if isinstance(payload, dict) and "image_bytes" in payload:
        return payload
    if isinstance(payload, (bytes, bytearray)):
        return {"image_bytes": bytes(payload)}
    raise TypeError("Unsupported image payload")


def normalize_text_result(text):
    return {"text": text or ""}
