import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client, subscription_path
from messaging_models import ConsumeResponse, normalize_payload


def consume_one() -> Optional[ConsumeResponse]:
    config = load_config()
    client = subscriber_client()
    sub_path = subscription_path(config.project_id, config.subscription_id)
    response = client.pull(subscription=sub_path, max_messages=1, timeout=5)
    if not response.received_messages:
        return None
    message = response.received_messages[0]
    payload = normalize_payload(message.message.data.decode("utf-8"))
    client.acknowledge(subscription=sub_path, ack_ids=[message.ack_id])
    return ConsumeResponse(message_id=message.message.message_id, payload=payload, attributes=dict(message.message.attributes))
