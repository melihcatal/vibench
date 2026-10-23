import os
from google.cloud import pubsub_v1

def publish_batch_messages(project_id: str, topic_id: str, messages: list[str]):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data in messages:
        # Data must be a bytestring
        data = message_data.encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)

    for future in futures:
        # Result() blocks until the message is published.
        print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Topic ID
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-project-id")
    TOPIC_ID = os.environ.get("GOOGLE_CLOUD_TOPIC_ID", "your-topic-id")

    # Example messages
    example_messages = [
        "Hello, Pub/Sub!",
        "This is a batch message.",
        "Another message in the batch.",
    ]

    print(f"Publishing messages to topic {TOPIC_ID} in project {PROJECT_ID}...")
    publish_batch_messages(PROJECT_ID, TOPIC_ID, example_messages)
    print("Batch publishing complete.")
