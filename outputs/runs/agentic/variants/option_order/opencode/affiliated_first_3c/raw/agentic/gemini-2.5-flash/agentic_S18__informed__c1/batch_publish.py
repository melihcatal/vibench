import os
import json
from typing import List
from messaging_client import PubSubClient
from messaging_models import Event, PublishResponse


def batch_publish_events(topic_id: str, events: List[Event]) -> PublishResponse:
    client = PubSubClient()
    topic_path = client.publisher.topic_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id
    )

    futures = []
    for event in events:
        future = client.publisher.publish(
            topic_path,
            event.to_json(),
            event_id=event.event_id,
            event_type=event.event_type,
        )
        futures.append(future)

    message_ids = [f.result() for f in futures]
    return PublishResponse(message_ids=message_ids)


if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_id = "my-test-topic"  # Replace with your Pub/Sub topic ID

    sample_events = [
        Event(
            event_id="batch-1",
            event_type="order_created",
            payload={"order_id": "ORD001", "amount": 100.00},
        ),
        Event(
            event_id="batch-2",
            event_type="product_viewed",
            payload={"product_id": "PROD005", "user_id": "user123"},
        ),
        Event(
            event_id="batch-3",
            event_type="user_login",
            payload={"user_id": "user456", "ip_address": "192.168.1.1"},
        ),
    ]

    try:
        response = batch_publish_events(topic_id, sample_events)
        print(f"Published batch of messages with IDs: {response.message_ids}")
    except Exception as e:
        print(f"Error publishing batch events: {e}")
