
from google.cloud import pubsub_v1
import os

def publish_batch_messages(project_id: str, topic_id: str, messages: list[tuple[str, dict | None]]):
    """Publishes a batch of messages to a Pub/Sub topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The Pub/Sub topic ID.
        messages: A list of tuples, where each tuple contains (message_data, attributes).
                  message_data should be a string, and attributes a dictionary or None.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data, attributes in messages:
        # Data must be a bytestring
        data = message_data.encode("utf-8")
        future = publisher.publish(topic_path, data, **(attributes if attributes else {}))
        futures.append(future)

    for future in futures:
        # Wait for the publish operation to complete
        message_id = future.result()
        print(f"Published message with ID: {message_id}")

if __name__ == "__main__":
    # Example Usage:
    # Set your Google Cloud Project ID and Pub/Sub Topic ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # gcloud is configured with appropriate credentials.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "your-pubsub-topic-id")

    # Example messages
    example_messages = [
        ("Hello, Pub/Sub!", {"origin": "python-script", "sequence": "1"}),
        ("Another message", {"type": "info"}),
        ("Message without attributes", None)
    ]

    if PROJECT_ID == "your-gcp-project-id" or TOPIC_ID == "your-pubsub-topic-id":
        print("Please set GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC_ID environment variables,")
        print("or replace 'your-gcp-project-id' and 'your-pubsub-topic-id' with actual values.")
    else:
        print(f"Publishing messages to topic: {TOPIC_ID} in project: {PROJECT_ID}")
        publish_batch_messages(PROJECT_ID, TOPIC_ID, example_messages)
