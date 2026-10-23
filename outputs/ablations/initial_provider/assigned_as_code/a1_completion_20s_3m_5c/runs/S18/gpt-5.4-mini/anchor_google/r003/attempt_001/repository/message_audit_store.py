from google.cloud import pubsub_v1


def message_audit_store(payload, config=None):
    client = pubsub_v1.SubscriberClient()
    try:
        record = dict(payload or {}) if isinstance(payload, dict) else {"value": payload}
        return {"stored": True, "record": record}
    finally:
        client.close()
