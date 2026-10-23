import os
import json
from google.cloud import pubsub_v1


def publish_event(event_data, topic_id=None):
    """Publishes a JSON event to a managed messaging topic or queue."""
    if topic_id is None:
        topic_id = os.environ.get(
            "PUBSUB_TOPIC_ID", "projects/my-project/topics/my-topic"
        )

    publisher = pubsub_v1.PublisherClient()

    # Convert event data to JSON string
    if isinstance(event_data, dict):
        data = json.dumps(event_data).encode("utf-8")
    else:
        data = str(event_data).encode("utf-8")

    # Publish the message
    future = publisher.publish(topic_id, data)
    message_id = future.result()

    return {"message_id": message_id, "topic": topic_id}


if __name__ == "__main__":
    # Example usage
    sample_event = {
        "event_type": "user_signup",
        "user_id": "user_123",
        "timestamp": "2023-10-01T12:00:00Z",
        "email": "user@example.com",
    }
    result = publish_event(sample_event)
    print(f"Published event with ID: {result['message_id']}")
