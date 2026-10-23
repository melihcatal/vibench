import json

from google.cloud import pubsub_v1

from messaging_client import get_subscriber_config
from messaging_models import normalize_received_message


def consume_event(payload, config=None):
    config = get_subscriber_config(config or {})
    client = pubsub_v1.SubscriberClient()
    subscription = client.subscription_path(config["project_id"], config["subscription_id"])
    response = client.pull(subscription=subscription, max_messages=1, timeout=config["timeout"])
    try:
        if not response.received_messages:
            return {"message": None}
        received = response.received_messages[0]
        message = normalize_received_message(received.message)
        client.acknowledge(subscription=subscription, ack_ids=[received.ack_id])
        return {"message": message, "attributes": dict(received.message.attributes), "data": json.loads(received.message.data.decode("utf-8"))}
    finally:
        client.close()
