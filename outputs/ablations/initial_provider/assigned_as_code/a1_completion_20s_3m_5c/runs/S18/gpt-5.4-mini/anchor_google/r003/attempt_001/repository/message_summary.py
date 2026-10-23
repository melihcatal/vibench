from google.cloud import pubsub_v1


def message_summary(payload, config=None):
    client = pubsub_v1.PublisherClient()
    try:
        data = payload.get("results", []) if isinstance(payload, dict) else []
        return {"count": len(data), "success": sum(1 for item in data if item.get("status") == "success")}
    finally:
        client.stop()
