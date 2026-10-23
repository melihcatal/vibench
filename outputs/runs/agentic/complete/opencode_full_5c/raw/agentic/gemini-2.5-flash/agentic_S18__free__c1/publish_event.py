from messaging_client import get_publisher_client, get_topic_path, get_project_id
from messaging_models import EventMessage
import json
import os


def publish_json_event(
    topic_id: str, event_data: dict, event_type: str, event_source: str
):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        event_data: The JSON payload of the event.
        event_type: The type of the event (e.g., "user.created").
        event_source: The source of the event (e.g., "webapp.userservice").
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    event_message = EventMessage(
        id=os.urandom(8).hex(),  # Generate a simple ID for this example
        type=event_type,
        source=event_source,
        data=event_data,
        attributes={"type": event_type, "source": event_source},
    )

    future = publisher.publish(
        topic_path, event_message.to_json(), **event_message.attributes
    )
    print(f"Published message ID: {future.result()}")


if __name__ == "__main__":
    # Example Usage (replace with your actual topic_id and data)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    example_topic_id = "my-test-topic"
    example_event_data = {"user_id": "123", "username": "testuser", "action": "created"}
    example_event_type = "user.created"
    example_event_source = "user-service"

    # publish_json_event(example_topic_id, example_event_data, example_event_type, example_event_source)
