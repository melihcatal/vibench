import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage


def publish_event(event_data: dict, topic_id: str = None) -> str:
    """Publish a JSON event to Google Cloud Pub/Sub topic."""
    if topic_id is None:
        topic_id = os.environ.get("PUBSUB_TOPIC_ID", "customer-events")

    publisher, project_id = get_pubsub_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    event_message = EventMessage.from_dict(event_data)
    serialized_data = json.dumps(event_message.to_dict()).encode("utf-8")

    future = publisher.publish(
        topic_path,
        serialized_data,
        event_type=event_message.event_type,
        customer_id=str(event_message.customer_id),
    )

    message_id = future.result()
    print(f"Published message {message_id} to {topic_path}")
    return message_id


if __name__ == "__main__":
    sample_event = {
        "event_type": "order_created",
        "customer_id": 12345,
        "timestamp": "2024-01-15T10:30:00Z",
        "payload": {"order_id": "ORD-789", "amount": 99.99},
    }
    publish_event(sample_event)
