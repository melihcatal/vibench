import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_subscription_path, load_settings
from messaging_models import ConsumeEventResponse, normalize_attributes


def consume_event(subscription_id: Optional[str] = None, ack: bool = True) -> ConsumeEventResponse:
    settings = load_settings()
    project_id = get_project_id(settings)
    subscription_path = get_subscription_path(project_id, subscription_id or settings.subscription_id)
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1}, timeout=10)
    if not response.received_messages:
        return ConsumeEventResponse(subscription=subscription_path, message_id=None, payload=None, attributes={}, acked=False)
    received = response.received_messages[0]
    payload = json.loads(received.message.data.decode("utf-8")) if received.message.data else None
    attributes = normalize_attributes(dict(received.message.attributes))
    if ack:
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})
    return ConsumeEventResponse(subscription=subscription_path, message_id=received.message.message_id, payload=payload, attributes=attributes, acked=ack)
