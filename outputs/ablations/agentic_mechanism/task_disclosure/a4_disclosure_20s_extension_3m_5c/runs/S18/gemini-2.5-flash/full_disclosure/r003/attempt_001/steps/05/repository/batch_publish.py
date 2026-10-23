import json
from google.cloud import pubsub_v1

def batch_publish_messages(project_id: str, topic_id: str, messages: list[dict]):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data in messages:
        # Messages must be bytestrings
        data = json.dumps(message_data["data"]).encode("utf-8")
        # Add attributes if provided
        attributes = message_data.get("attributes")
        if attributes:
            future = publisher.publish(topic_path, data, **attributes)
        else:
            future = publisher.publish(topic_path, data)
        futures.append(future)

    for future in futures:
        # Result() blocks until the message is published.
        print(f"Published message ID: {future.result()}")

