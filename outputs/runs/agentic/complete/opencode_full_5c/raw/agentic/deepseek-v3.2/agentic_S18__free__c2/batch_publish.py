import os
from google.cloud import pubsub_v1
import json
from typing import List, Dict, Any, Tuple
import uuid


def publish_batch(
    messages: List[Dict[str, Any]], topic_id: str = None
) -> List[Tuple[str, str]]:
    """Publish a batch of messages to Google Cloud Pub/Sub with IDs and attributes."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if topic_id is None:
        topic_id = os.environ.get("PUBSUB_TOPIC_ID", "customer-events")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    results = []

    for message_data in messages:
        message_id = str(uuid.uuid4())
        data = json.dumps(message_data).encode("utf-8")

        future = publisher.publish(
            topic_path,
            data,
            message_id=message_id,
            batch_index=str(len(results)),
            total_messages=str(len(messages)),
        )

        published_id = future.result()
        results.append((message_id, published_id))

    return results


if __name__ == "__main__":
    batch_messages = [
        {
            "event_type": "order_created",
            "order_id": "ord_001",
            "customer_id": "cust_12345",
            "amount": 49.99,
        },
        {
            "event_type": "order_created",
            "order_id": "ord_002",
            "customer_id": "cust_67890",
            "amount": 129.99,
        },
        {
            "event_type": "order_created",
            "order_id": "ord_003",
            "customer_id": "cust_54321",
            "amount": 24.99,
        },
    ]

    try:
        results = publish_batch(batch_messages)
        print(f"Published {len(results)} messages:")
        for client_id, server_id in results:
            print(f"  Client ID: {client_id} -> Server ID: {server_id}")
    except Exception as e:
        print(f"Failed to publish batch: {e}")
