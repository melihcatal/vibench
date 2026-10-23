def normalize_text(value):
    if value is None:
        return ""
    return str(value)


def normalize_messages(messages):
    return [{"role": m.get("role", "user"), "content": normalize_text(m.get("content", ""))} for m in (messages or [])]


def normalize_payload(payload):
    return payload or {}
