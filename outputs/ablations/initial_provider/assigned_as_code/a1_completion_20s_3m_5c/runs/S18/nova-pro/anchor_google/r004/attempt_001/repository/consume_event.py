import json

from google.cloud import pubsub_v1

from messaging_client import get_pubsub_client


def consume_event(config=None):
    config = config or {}
    client = get_pubsub_client(config["project_id"])
    subscription = client.subscription_path(config["project_id"], config["subscription_id"])
    response = client.pull(subscription, max_messages=1)
    if response.received_messages:
        message = response.received_messages[0]
        data = json.loads(message.message.data.decode("utf-8"))
        client.acknowledge(subscription, [message.ack_id])
        return data
    return None