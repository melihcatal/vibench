import os
from messaging_client import PubSubClient
from messaging_models import EventMessage


def publish_json_event(topic_id: str, event: EventMessage):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    publisher = client.get_publisher_client()
    topic_path = publisher.topic_path(client.project_id, topic_id)

    future = publisher.publish(topic_path, event.to_json(), **(event.attributes or {}))
    message_id = future.result()
    print(f"Published message {message_id} to topic {topic_id}")
    return message_id


if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Create a topic first, e.g., 'my-test-topic'
    # gcloud pubsub topics create my-test-topic

    topic_id = os.getenv("PUBSUB_TOPIC_ID", "my-test-topic")
    sample_event = EventMessage(
        id="event-123",
        data={
            "action": "user_created",
            "user_id": "alice",
            "timestamp": "2023-10-27T10:00:00Z",
        },
        attributes={"origin": "webapp", "version": "1.0"},
    )
    publish_json_event(topic_id, sample_event)
