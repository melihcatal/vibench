from google.cloud import pubsub_v1

def publish_batch_messages(project_id: str, topic_id: str, messages: list[str]):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message in messages:
        # Data must be a bytestring
        data = message.encode("utf-8")
        futures.append(publisher.publish(topic_path, data))

    for future in futures:
        # Result() waits for the publish to complete.
        print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Topic ID
    PROJECT_ID = "your-gcp-project-id"  
    TOPIC_ID = "your-pubsub-topic-id" 
    MESSAGES = [
        "First message in batch",
        "Second message in batch",
        "Third message in batch"
    ]

    publish_batch_messages(PROJECT_ID, TOPIC_ID, MESSAGES)
