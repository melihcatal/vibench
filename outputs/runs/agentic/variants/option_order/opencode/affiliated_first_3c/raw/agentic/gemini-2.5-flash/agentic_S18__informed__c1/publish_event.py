import os
from messaging_client import PubSubClient
from messaging_models import Event, PublishResponse


def publish_event(topic_id: str, event: Event) -> PublishResponse:
    client = PubSubClient()
    topic_path = client.publisher.topic_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id
    )
    future = client.publisher.publish(
        topic_path,
        event.to_json(),
        event_id=event.event_id,
        event_type=event.event_type,
    )
    return PublishResponse(message_ids=[future.result()])


if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_id = "my-test-topic"  # Replace with your Pub/Sub topic ID

    sample_event = Event(
        event_id="12345",
        event_type="user_signup",
        payload={"username": "testuser", "email": "test@example.com"},
    )

    try:
        response = publish_event(topic_id, sample_event)
        print(f"Published message with ID: {response.message_ids[0]}")
    except Exception as e:
        print(f"Error publishing event: {e}")
