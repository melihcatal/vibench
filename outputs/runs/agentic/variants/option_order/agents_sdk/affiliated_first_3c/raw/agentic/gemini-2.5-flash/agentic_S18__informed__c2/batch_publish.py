import json
import os
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client

def publish_batch_events(topic_id: str, messages: list[dict], project_id: str = None):
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id or os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)

    futures = []
    for msg_data in messages:
        json_data = json.dumps(msg_data["data"]).encode("utf-8")
        attributes = msg_data.get("attributes", {})
        future = publisher.publish(topic_path, json_data, **attributes)
        futures.append(future)

    for future in futures:
        print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var set)
    # Ensure a topic named 'my-topic' exists in your project.
    # from your shell, run:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python batch_publish.py
    batch_of_events = [
        {"data": {"event_type": "user_created", "user_id": "1"}, "attributes": {"source": "web"}},
        {"data": {"event_type": "product_viewed", "product_id": "P001"}, "attributes": {"source": "mobile"}},
        {"data": {"event_type": "order_placed", "order_id": "ORD999"}, "attributes": {"source": "api"}}
    ]
    publish_batch_events("my-topic", batch_of_events)
