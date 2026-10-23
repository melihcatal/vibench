import json
from messaging_client import get_pubsub_subscriber, resolve_subscription_path
from messaging_models import decode_pubsub_message, success_result


def consume_event(project_id=None, subscription_id=None, timeout=10):
    subscriber = get_pubsub_subscriber()
    subscription_path = resolve_subscription_path(project_id, subscription_id)
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1}, timeout=timeout)
    received = response.received_messages
    if not received:
        return success_result(provider="google_cloud_pubsub", operation="consume_event", message=None, subscription=subscription_path)
    message = received[0].message
    ack_id = received[0].ack_id
    payload = decode_pubsub_message(message)
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [ack_id]})
    return success_result(provider="google_cloud_pubsub", operation="consume_event", message=payload, subscription=subscription_path)
