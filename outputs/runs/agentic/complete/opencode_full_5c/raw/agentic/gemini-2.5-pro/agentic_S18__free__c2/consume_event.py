import os
import json
from typing import Optional

from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import ReceivedMessage, Message


def consume_one_event(subscription_id: str) -> Optional[ReceivedMessage]:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]

    try:
        data = json.loads(received_message.message.data.decode("utf-8"))
    except json.JSONDecodeError:
        data = {"raw": received_message.message.data.decode("utf-8")}

    msg = ReceivedMessage(
        ack_id=received_message.ack_id,
        message=Message(
            data=data,
            attributes=dict(received_message.message.attributes),
            message_id=received_message.message.message_id,
        ),
        delivery_attempt=received_message.delivery_attempt,
    )

    print(f"Received message: {msg.message.message_id}")

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [msg.ack_id]}
    )
    print(f"Acknowledged message: {msg.message.message_id}")

    return msg


if __name__ == "__main__":
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("PUBSUB_SUBSCRIPTION_ID environment variable not set.")

    consume_one_event(subscription_id)
