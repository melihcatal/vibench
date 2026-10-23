from google.cloud import pubsub_v1


def payload_translate(payload, config=None):
    client = pubsub_v1.PublisherClient()
    try:
        text = (payload or {}).get("text", "") if isinstance(payload, dict) else str(payload)
        return {"text": text}
    finally:
        client.stop()
