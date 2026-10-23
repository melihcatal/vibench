import os
import json
from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import Message, ReceivedMessage


def consume_one_message():
    subscriber = get_subscriber_client()
    subscription_id = os.environ.get("GCP_SUBSCRIPTION_ID", "my-subscription")
    subscription_path = get_subscription_path(subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
        timeout=30.0,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]

    msg_data = json.loads(received.message.data)

    message = Message(
        data=msg_data,
        attributes=dict(received.message.attributes),
        message_id=received.message.message_id,
    )

    received_message = ReceivedMessage(
        ack_id=received.ack_id,
        message=message,
        delivery_attempt=received.delivery_attempt,
    )

    # Acknowledge the message so it's not delivered again
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [received.ack_id]}
    )

    return received_message


if __name__ == "__main__":
    print("Consuming one message...")
    msg = consume_one_message()
    if msg:
        print(f"Consumed message: {msg.message.data}")
    else:
        print("No messages in subscription.")
