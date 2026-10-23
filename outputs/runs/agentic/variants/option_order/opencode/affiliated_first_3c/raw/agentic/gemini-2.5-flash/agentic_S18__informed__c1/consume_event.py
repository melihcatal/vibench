import os
import json
from messaging_client import PubSubClient
from messaging_models import ConsumeResponse, PubSubMessage


def consume_event(subscription_id: str, timeout: int = 5) -> ConsumeResponse:
    client = PubSubClient()
    subscription_path = client.subscriber.subscription_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), subscription_id
    )

    response = client.subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}, timeout=timeout
    )

    if response.received_messages:
        received_message = response.received_messages[0]
        message = PubSubMessage(
            data=received_message.message.data,
            attributes=dict(received_message.message.attributes),
            message_id=received_message.message.message_id,
        )
        return ConsumeResponse(message=message, ack_id=received_message.ack_id)
    return ConsumeResponse()


if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    subscription_id = (
        "my-test-subscription"  # Replace with your Pub/Sub subscription ID
    )

    try:
        response = consume_event(subscription_id)
        if response.message:
            print(f"Received message: {response.message.message_id}")
            print(f"Data: {response.message.data.decode('utf-8')}")
            print(f"Attributes: {response.message.attributes}")
            # Acknowledge the message
            pubsub_client = PubSubClient()
            pubsub_client.subscriber.acknowledge(
                request={
                    "subscription": pubsub_client.subscriber.subscription_path(
                        project_id, subscription_id
                    ),
                    "ack_ids": [response.ack_id],
                }
            )
            print("Message acknowledged.")
        else:
            print("No messages received.")
    except Exception as e:
        print(f"Error consuming event: {e}")
