import json
import uuid
import os
from typing import List, Dict
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage


def publish_batch(messages: List[Dict], topic_id: str = None) -> List[str]:
    """Publish a batch of messages to Google Cloud Pub/Sub with IDs and attributes."""
    if topic_id is None:
        topic_id = os.environ.get("PUBSUB_TOPIC_ID", "customer-events")

    publisher, project_id = get_pubsub_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    message_ids = []

    for msg_data in messages:
        event_message = EventMessage.from_dict(msg_data)
        serialized_data = json.dumps(event_message.to_dict()).encode("utf-8")

        message_id = str(uuid.uuid4())

        future = publisher.publish(
            topic_path,
            serialized_data,
            message_id=message_id,
            event_type=event_message.event_type,
            customer_id=str(event_message.customer_id),
            batch_index=str(len(futures)),
        )

        futures.append(future)

    for future in futures:
        pubsub_message_id = future.result()
        message_ids.append(pubsub_message_id)

    print(f"Published batch of {len(message_ids)} messages to {topic_path}")
    return message_ids


def create_sample_batch(count: int = 5) -> List[Dict]:
    """Create a sample batch of messages for testing."""
    messages = []
    for i in range(count):
        messages.append(
            {
                "event_type": f"order_created_{i}",
                "customer_id": 10000 + i,
                "timestamp": "2024-01-15T10:30:00Z",
                "payload": {
                    "order_id": f"ORD-{1000 + i}",
                    "amount": 50.0 + (i * 10),
                    "items": i + 1,
                },
            }
        )
    return messages


if __name__ == "__main__":
    sample_batch = create_sample_batch(3)
    message_ids = publish_batch(sample_batch)
    print(f"Published message IDs: {message_ids}")
