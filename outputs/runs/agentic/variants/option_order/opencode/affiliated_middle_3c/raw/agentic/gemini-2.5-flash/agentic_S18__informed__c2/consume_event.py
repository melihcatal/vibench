import json
from messaging_client import (
    get_subscriber_client,
    get_project_id,
    get_subscription_path,
)
from messaging_models import PubSubMessage


def consume_event(subscription_id: str, timeout: float = 5.0):
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = get_subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        retry=None,
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    ack_id = received_message.ack_id
    message_data = json.loads(received_message.message.data.decode("utf-8"))
    message_id = received_message.message.message_id
    message_attributes = dict(received_message.message.attributes)

    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
        }
    )

    print(f"Consumed message ID: {message_id}")
    return PubSubMessage(message_data, message_id, message_attributes)
