import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client, subscription_path
from messaging_models import ConsumeEventResponse, normalize_attributes


def consume_one_message() -> Optional[ConsumeEventResponse]:
    cfg = load_config()
    client = subscriber_client()
    sub_path = subscription_path(cfg.subscription_id)
    response = client.pull(subscription=sub_path, max_messages=1, timeout=5.0)
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    data = json.loads(received.message.data.decode("utf-8"))
    attributes = normalize_attributes(received.message.attributes)
    client.acknowledge(subscription=sub_path, ack_ids=[received.ack_id])
    return ConsumeEventResponse(
        message_id=received.message.message_id,
        data=data,
        attributes=attributes,
        acked=True,
    )
