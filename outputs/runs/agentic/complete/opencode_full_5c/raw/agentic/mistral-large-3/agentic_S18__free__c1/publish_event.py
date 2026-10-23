from google.cloud import pubsub_v1
import json
import os

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
topic_id = os.getenv("GOOGLE_CLOUD_TOPIC_ID")

# Initialize Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def publish_event(event_data: dict) -> str:
    """
    Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event_data: Dictionary containing event data to publish.

    Returns:
        str: The message ID of the published message.
    """
    # Convert event data to JSON string
    data = json.dumps(event_data).encode("utf-8")

    # Publish the message
    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return message_id
