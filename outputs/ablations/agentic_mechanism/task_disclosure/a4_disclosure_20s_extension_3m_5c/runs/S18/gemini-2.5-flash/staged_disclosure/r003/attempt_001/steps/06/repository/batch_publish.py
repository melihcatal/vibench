
from google.cloud import pubsub_v1
import os

def publish_batch_messages(project_id: str, topic_id: str, messages: list):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data in messages:
        # message_data can be a string or bytes.
        # If it's a string, encode it to bytes.
        if isinstance(message_data, str):
            message_data = message_data.encode("utf-8")
        future = publisher.publish(topic_path, message_data)
        futures.append(future)

    for future in futures:
        future.result() # Wait for the publish operation to complete
    print(f"Published {len(messages)} messages to {topic_path}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Topic ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # gcloud is configured with appropriate authentication.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = "my-topic" # Replace with your Pub/Sub topic ID

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Example messages
        example_messages = [
            "Hello, Pub/Sub!",
            "This is another message.",
            "Batch publishing is efficient."
        ]
        publish_batch_messages(project_id, topic_id, example_messages)
