from google.cloud import pubsub_v1


def message_safety(payload, config=None):
    client = pubsub_v1.SubscriberClient()
    try:
        text = (payload or {}).get("text", "") if isinstance(payload, dict) else str(payload)
        unsafe = any(token in text.lower() for token in ["password", "secret", "ssn"])
        return {"safe": not unsafe}
    finally:
        client.close()
