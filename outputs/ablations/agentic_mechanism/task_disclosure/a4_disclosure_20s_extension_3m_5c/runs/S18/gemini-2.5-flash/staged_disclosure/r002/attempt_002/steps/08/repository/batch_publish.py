
from google.cloud import pubsub_v1
import os

def publish_batch_messages(project_id: str, topic_id: str, messages: list[str]):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data in messages:
        # Data must be a bytestring
        data = message_data.encode("utf-8")
        futures.append(publisher.publish(topic_path, data))

    for future in futures:
        print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Topic ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = "my-test-topic"  # Replace with your Pub/Sub topic ID

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        sample_messages = [
            "message 1",
            "message 2",
            "message 3"
        ]
        print(f"Publishing messages to topic '{topic_id}' in project '{project_id}'...")
        publish_batch_messages(project_id, topic_id, sample_messages)
        print("Batch publishing complete.")
