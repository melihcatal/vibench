import json
from google.cloud import pubsub_v1
from messaging_client import load_config, subscription_path


def consume_event():
    config = load_config()
    client = pubsub_v1.SubscriberClient()
    response = client.pull(
        request={
            "subscription": subscription_path(
                config.project_id, config.subscription_id
            ),
            "max_messages": 1,
        }
    )
    if not response.received_messages:
        return None
    message = response.received_messages[0]
    payload = json.loads(message.message.data.decode("utf-8"))
    client.acknowledge(
        request={
            "subscription": subscription_path(
                config.project_id, config.subscription_id
            ),
            "ack_ids": [message.ack_id],
        }
    )
    return {
        "ack_id": message.ack_id,
        "message_id": message.message.message_id,
        "payload": payload,
        "attributes": dict(message.message.attributes),
    }
