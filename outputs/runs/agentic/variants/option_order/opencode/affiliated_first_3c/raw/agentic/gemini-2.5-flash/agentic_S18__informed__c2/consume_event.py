import time
import os

from messaging_client import PubSubClient
from messaging_models import PubsubMessage, ConsumeResponse


def consume_event(subscription_id: str, timeout: int = 5) -> ConsumeResponse:
    client = PubSubClient()
    subscription_path = client.get_subscription_path(subscription_id)

    response = client.subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )

    if not response.received_messages:
        return ConsumeResponse(message=None)

    received_message = response.received_messages[0]
    message = received_message.message
    ack_id = received_message.ack_id

    pubsub_message = PubsubMessage(
        data=message.data,
        attributes=dict(message.attributes),
        message_id=message.message_id,
        publish_time=message.publish_time.isoformat() if message.publish_time else None,
    )

    # Acknowledge the message to remove it from the subscription
    client.subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]}
    )

    return ConsumeResponse(message=pubsub_message, ack_id=ack_id)


if __name__ == "__main__":
    # Example Usage (requires GOOGLE_CLOUD_PROJECT environment variable set)
    # and a Pub/Sub subscription named 'my-subscription'
    subscription_id = "my-subscription"

    print(f"Listening for messages on {subscription_id}...")
    response = consume_event(subscription_id)

    if response.message:
        print(f"Received message: {response.message.to_json()}")
        print(f"Acknowledged with ack_id: {response.ack_id}")
    else:
        print("No messages received.")
