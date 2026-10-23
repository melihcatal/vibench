import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_subscriber_client

def process_message_with_dead_letter(subscription_id: str, dead_letter_topic_id: str, timeout: int = 5):
    """Consumes a message and, if processing fails, publishes it to a dead-letter topic."""
    subscriber = get_subscriber_client()
    publisher = get_publisher_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Attempting to process message: {message.message_id}")
        try:
            # Simulate message processing
            payload = message.data.decode('utf-8')
            if "fail" in payload.lower():
                raise ValueError("Simulated processing failure")

            print(f"Successfully processed message: {message.message_id} with data: {payload}")
            message.ack()
        except Exception as e:
            print(f"Processing failed for message {message.message_id}: {e}")
            print(f"Publishing message {message.message_id} to dead-letter topic: {dead_letter_topic_id}")
            try:
                # Re-publish to dead-letter topic
                future = publisher.publish(dead_letter_topic_path, message.data, **message.attributes)
                future.result() # Ensure publish completes
                print(f"Message {message.message_id} sent to dead-letter topic. New ID: {future.result()}")
                message.ack() # Acknowledge original message once sent to DLQ
            except Exception as dl_e:
                print(f"Failed to send message {message.message_id} to dead-letter topic: {dl_e}")
                message.nack() # Negative acknowledge if cannot even move to DLQ

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path} with dead-lettering to {dead_letter_topic_id}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        print(f"Listening for messages on {subscription_path} threw an exception: {e}.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS)
    # Ensure main subscription "my-event-subscription" and dead-letter topic "my-dead-letter-topic" exist.
    # You can publish messages with '{"message": "This should fail"}' to test the dead-letter path.
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python dead_letter.py
    main_subscription_id = "my-event-subscription"
    dl_topic_id = "my-dead-letter-topic"
    process_message_with_dead_letter(main_subscription_id, dl_topic_id)
