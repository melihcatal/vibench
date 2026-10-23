from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_subscriber_client, get_subscription_path, load_settings
from messaging_models import ConsumeEventResponse, normalize_received_message


def consume_event(request: Dict[str, Any]) -> Dict[str, Any]:
    settings = load_settings()
    client = get_subscriber_client()
    subscription_path = get_subscription_path(client, settings.project_id, settings.subscription_id)
    response = client.pull(subscription=subscription_path, max_messages=1, timeout=settings.timeout_seconds)
    if not response.received_messages:
        return ConsumeEventResponse.empty(subscription_path).to_dict()
    received = response.received_messages[0]
    message = normalize_received_message(received.message)
    client.acknowledge(subscription=subscription_path, ack_ids=[received.ack_id])
    return ConsumeEventResponse.from_message(subscription_path, received.ack_id, message).to_dict()
