import json
from google.cloud import pubsub_v1
from messaging_client import get_subscriber, get_subscription_path
from messaging_models import normalize_consume_result

def consume_event(subscription=None, timeout=5.0):
    subscriber = get_subscriber()
    subscription_path = subscription or get_subscription_path()
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True}, timeout=timeout)
    messages = []
    for received in response.received_messages:
        payload = received.message.data.decode("utf-8") if received.message.data else ""
        messages.append(normalize_consume_result(message_id=received.message.message_id, payload=json.loads(payload) if payload else {}, attributes=dict(received.message.attributes)))
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})
        break
    return messages[0] if messages else None
