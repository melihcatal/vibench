import json

from google.cloud import pubsub_v1

from messaging_client import create_subscriber_client, load_pubsub_config, subscription_path
from messaging_models import build_message_record


def consume_event(payload, config=None):
    config = load_pubsub_config(config)
    client = create_subscriber_client()
    sub_path = subscription_path(client, config["project_id"], config["subscription_id"])
    response = client.pull(subscription=sub_path, max_messages=1, timeout=30)
    if not response.received_messages:
        client.close()
        return build_message_record(status="empty")
    received = response.received_messages[0]
    data = received.message.data.decode("utf-8") if received.message.data else ""
    attributes = dict(received.message.attributes)
    client.acknowledge(subscription=sub_path, ack_ids=[received.ack_id])
    client.close()
    return build_message_record(message_id=received.message.message_id, payload=json.loads(data) if data else None, attributes=attributes, status="consumed")
