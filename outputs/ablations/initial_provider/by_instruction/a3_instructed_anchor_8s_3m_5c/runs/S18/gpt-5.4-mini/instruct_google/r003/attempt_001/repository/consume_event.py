from messaging_client import decode_json, subscriber_client, subscription_path


def consume_event(subscription: str):
    client = subscriber_client()
    response = client.pull(request={"subscription": subscription_path(subscription), "max_messages": 1}, timeout=10)
    messages = response.received_messages
    if not messages:
        return {"provider": "google.pubsub_v1", "subscription": subscription_path(subscription), "message": None}
    received = messages[0]
    payload = decode_json(received.message.data)
    client.acknowledge(request={"subscription": subscription_path(subscription), "ack_ids": [received.ack_id]})
    return {"provider": "google.pubsub_v1", "subscription": subscription_path(subscription), "message_id": received.message.message_id, "payload": payload}
