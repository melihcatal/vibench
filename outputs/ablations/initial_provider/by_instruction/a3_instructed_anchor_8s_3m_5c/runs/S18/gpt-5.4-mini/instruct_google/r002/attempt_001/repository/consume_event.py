import json

from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client, subscription_path
from messaging_models import message_to_dict


def consume_event():
    config = load_config()
    client = subscriber_client()
    subscription = subscription_path(config)
    response = client.pull(subscription=subscription, max_messages=1)
    if not response.received_messages:
        return {"message": None}
    received = response.received_messages[0]
    client.acknowledge(subscription=subscription, ack_ids=[received.ack_id])
    return message_to_dict(received.message)


if __name__ == "__main__":
    print(json.dumps(consume_event()))
