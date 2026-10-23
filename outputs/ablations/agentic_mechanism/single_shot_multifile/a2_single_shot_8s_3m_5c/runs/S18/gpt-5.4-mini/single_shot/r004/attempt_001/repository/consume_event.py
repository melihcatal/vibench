import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_subscription_path, get_subscriber_client
from messaging_models import normalize_consumed_message


def consume_event(ack: bool = True) -> Dict[str, Any]:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path()
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True})
    if not response.received_messages:
        return {"message": None, "subscription_path": subscription_path}
    received = response.received_messages[0]
    payload = normalize_consumed_message(received.message.data, received.message.attributes)
    if ack:
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})
    return {"message": payload, "ack_id": received.ack_id, "subscription_path": subscription_path}
