from messaging_client import (
    get_subscriber_client,
    get_subscription_path,
    get_project_id,
)
from messaging_models import EventMessage
import time
import os


def consume_one_event(subscription_id: str, timeout: int = 5):
    """Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        An EventMessage object if a message is consumed, otherwise None.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    # The subscriber pulls messages synchronously. This is suitable for consuming one message.
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": True,
        }
    )

    if response.received_messages:
        received_message = response.received_messages[0]
        ack_id = received_message.ack_id
        message = received_message.message

        event_message = EventMessage.from_pubsub_message(message)

        # Acknowledge the message so it is not redelivered.
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [ack_id]}
        )

        print(f"Received and acknowledged message: {event_message.id}")
        return event_message
    else:
        print("No messages received.")
        return None


if __name__ == "__main__":
    # Example Usage (replace with your actual subscription_id)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    example_subscription_id = "my-test-subscription"

    # event = consume_one_event(example_subscription_id)
    # if event:
    #     print(f"Event Data: {event.data}")
