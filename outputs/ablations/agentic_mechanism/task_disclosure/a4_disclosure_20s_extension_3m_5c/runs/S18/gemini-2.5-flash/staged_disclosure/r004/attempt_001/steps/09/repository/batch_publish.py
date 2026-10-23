
from google.cloud import pubsub_v1

def publish_batch_messages(project_id: str, topic_id: str, messages: list[str]):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message in messages:
        # Data must be a bytestring
        data = message.encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)

    for future in futures:
        # Result() blocks until the publish future is resolved
        print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Replace with your Google Cloud project ID and topic ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    PROJECT_ID = "your-project-id"
    TOPIC_ID = "your-topic-id"
    
    # Example messages to publish
    MESSAGES = [
        "Hello from message 1!",
        "Hello from message 2!",
        "Hello from message 3!",
    ]

    print(f"Publishing {len(MESSAGES)} messages to topic {TOPIC_ID} in project {PROJECT_ID}...")
    publish_batch_messages(PROJECT_ID, TOPIC_ID, MESSAGES)
    print("Batch publishing complete.")
