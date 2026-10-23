import json
from messaging_client import MessagingClient


def publish_event(topic_name: str, event: dict) -> None:
    """Publish a JSON payload to a managed Pub/Sub topic.

    Uses Google Cloud Pub/Sub as the concrete messaging provider.
    The provider is identifiable through the Google Cloud Pub/Sub library import
    and the usage of `publisher.publish` with a fully qualified topic name.
    """
    client = MessagingClient()
    # Fully qualified topic name format: projects/{project}/topics/{topic}
    full_topic = f"projects/{client.project_id}/topics/{topic_name}"
    # Convert event dict to JSON string
    message_data = json.dumps(event).encode("utf-8")
    # Publish message
    client.publisher.publish(full_topic, data=message_data)
    print(f"Published event to {full_topic}")
