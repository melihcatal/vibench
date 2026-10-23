from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client, subscription_path
from messaging_models import parse_pubsub_message


def consume_event(payload=None, config=None):
    config = load_config(config)
    client = subscriber_client()
    subscription = subscription_path(client, config["project_id"], config["subscription_id"])
    response = client.pull(request={"subscription": subscription, "max_messages": 1, "return_immediately": True})
    try:
        if not response.received_messages:
            return {"message": None}
        received = response.received_messages[0]
        message = parse_pubsub_message(received.message)
        client.acknowledge(request={"subscription": subscription, "ack_ids": [received.ack_id]})
        return {"message": message}
    finally:
        client.close()
