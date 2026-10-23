def normalize_received_message(message, payload):
    return {
        "message_id": getattr(message, "message_id", None),
        "body": payload,
        "content_type": getattr(message, "content_type", None),
        "application_properties": dict(getattr(message, "application_properties", {}) or {}),
    }
