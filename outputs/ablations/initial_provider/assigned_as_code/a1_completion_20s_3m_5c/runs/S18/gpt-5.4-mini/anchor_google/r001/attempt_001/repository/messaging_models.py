def normalize_event_payload(payload):
    if isinstance(payload, dict) and "event" in payload:
        return payload["event"]
    return payload


def normalize_received_message(message):
    data = message.data.decode("utf-8") if getattr(message, "data", None) else ""
    return {
        "message_id": getattr(message, "message_id", None),
        "publish_time": str(getattr(message, "publish_time", "")),
        "data": data,
        "attributes": dict(getattr(message, "attributes", {})),
    }


def normalize_batch_items(messages):
    items = []
    for message in messages:
        if isinstance(message, dict):
            items.append({"event": normalize_event_payload(message), "message_id": message.get("message_id"), "source": message.get("source")})
        else:
            items.append({"event": message})
    return items
