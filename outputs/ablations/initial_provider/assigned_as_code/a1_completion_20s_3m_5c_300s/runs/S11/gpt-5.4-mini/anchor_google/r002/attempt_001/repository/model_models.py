def normalize_text_payload(payload):
    if isinstance(payload, dict):
        return payload.get("text", "")
    return str(payload or "")


def build_response(text, **metadata):
    response = {"text": text or ""}
    response.update(metadata)
    return response
