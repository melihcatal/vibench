def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def payload_text(payload):
    if isinstance(payload, dict):
        if "text" in payload:
            return payload["text"]
        if "input" in payload:
            return payload["input"]
    return payload
