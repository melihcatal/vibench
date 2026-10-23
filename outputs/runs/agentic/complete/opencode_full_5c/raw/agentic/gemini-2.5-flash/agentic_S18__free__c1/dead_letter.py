from messaging_client import (
    get_publisher_client,
    get_subscriber_client,
    get_topic_path,
    get_subscription_path,
    get_project_id,
)
from messaging_models import EventMessage
import json
import os
import time


def process_and_handle_dead_letter(
    subscription_id: str, dead_letter_topic_id: str, simulate_failure: bool = False
):
    """Consumes a message, simulates processing, and sends to DLQ on failure.

    Args:
        subscription_id: The ID of the Pub/Sub subscription to consume from.
        dead_letter_topic_id: The ID of the dead-letter Pub/Sub topic.
        simulate_failure: If True, simulates a processing failure.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_path(project_id, dead_letter_topic_id)

    print(f"Listening for messages on {subscription_path}...")

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

        print(f"Received message ID: {event_message.id}")
        print(f"Message data: {event_message.data}")

        try:
            if simulate_failure:
                raise RuntimeError("Simulated processing failure!")

            # Simulate successful processing
            print(f"Successfully processed message {event_message.id}.")
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )

        except Exception as e:
            print(f"Error processing message {event_message.id}: {e}")
            # Send to dead-letter topic
            dlq_attributes = event_message.attributes or {}
            dlq_attributes["dlq_reason"] = str(e)
            dlq_attributes["original_topic"] = (
                topic_id  # Assuming original topic from subscription context
            )

            future = publisher.publish(
                dead_letter_topic_path, event_message.to_json(), **dlq_attributes
            )
            print(
                f"Sent message {event_message.id} to DLQ with message ID: {future.result()}"
            )
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )
    else:
        print("No messages received to process.")


if __name__ == "__main__":
    # Example Usage (replace with your actual IDs)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    example_subscription_id = "my-test-subscription"
    example_dead_letter_topic_id = "my-dead-letter-topic"
    example_topic_id = "my-test-topic"  # Assuming the original topic

    # To simulate success:
    # process_and_handle_dead_letter(example_subscription_id, example_dead_letter_topic_id, simulate_failure=False)

    # To simulate failure:
    # process_and_handle_dead_letter(example_subscription_id, example_dead_letter_topic_id, simulate_failure=True)
