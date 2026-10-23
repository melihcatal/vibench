def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    return {"text": payload.get("text", ""), **payload}


def normalize_messages(payload):
    payload = payload or {}
    messages = payload.get("messages", [])
    normalized = []
    for index, message in enumerate(messages):
        if isinstance(message, str):
            normalized.append({"id": str(index), "text": message})
        else:
            normalized.append({"id": str(message.get("id", index)), "text": message.get("text", "")})
    return {"messages": normalized}
