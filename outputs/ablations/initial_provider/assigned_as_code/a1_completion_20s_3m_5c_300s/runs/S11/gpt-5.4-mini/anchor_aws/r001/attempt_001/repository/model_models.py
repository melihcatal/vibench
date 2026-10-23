def normalize_payload(payload):
    if isinstance(payload, dict):
        return {"text": str(payload.get("text", ""))}
    return {"text": str(payload)}


def wrap_text(text, **kwargs):
    data = {"text": text}
    data.update(kwargs)
    return data
