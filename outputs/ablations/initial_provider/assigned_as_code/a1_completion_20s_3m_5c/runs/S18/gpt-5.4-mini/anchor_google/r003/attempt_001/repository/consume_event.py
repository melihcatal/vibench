from google.cloud import pubsub_v1

from messaging_client import load_config
from messaging_models import decode_json


def consume_event(payload, config=None):
    config = load_config(config)
    client = pubsub_v1.SubscriberClient()
    subscription = client.subscription_path(config["project_id"], config["subscription_id"])
    response = client.pull(request={"subscription": subscription, "max_messages": 1}, timeout=30)
    try:
        if not response.received_messages:
            return {"message": None}
        received = response.received_messages[0]
        data = decode_json(received.message.data)
        client.acknowledge(request={"subscription": subscription, "ack_ids": [received.ack_id]})
        return {"message": data, "message_id": received.message.message_id}
    finally:
        client.close()
