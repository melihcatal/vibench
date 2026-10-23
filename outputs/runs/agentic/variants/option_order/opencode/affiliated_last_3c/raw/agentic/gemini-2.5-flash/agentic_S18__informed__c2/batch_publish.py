import os
import json
from typing import List, Dict, Any
from messaging_client import PubSubClient
from messaging_models import PubSubMessage


def batch_publish_events(
    topic_name: str, events_data: List[Dict[str, Any]]
) -> List[str]:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    messages = []
    for i, event_data in enumerate(events_data):
        # Assuming message_id and attributes can be derived or are part of event_data if needed
        attributes = event_data.pop("attributes", {})
        message = PubSubMessage(data=event_data, attributes=attributes)
        messages.append(message)

    message_ids = client.publish_batch(topic_name, messages)
    print(f"Published {len(message_ids)} messages in batch to topic: {topic_name}")
    return message_ids


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to a path of your service account key file
    # Create a topic named 'my-batch-topic' in your Google Cloud project

    # Make sure to set environment variables:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    example_topic_name = os.environ.get("PUBSUB_BATCH_TOPIC_NAME", "my-batch-topic")
    example_events = [
        {
            "event_type": "user_created",
            "user_id": "1",
            "name": "Alice",
            "attributes": {"source": "web"},
        },
        {
            "event_type": "product_viewed",
            "product_id": "P101",
            "user_id": "1",
            "attributes": {"source": "app"},
        },
        {
            "event_type": "cart_updated",
            "user_id": "2",
            "items": [{"id": "P102", "qty": 1}],
            "attributes": {"source": "web"},
        },
    ]

    try:
        published_ids = batch_publish_events(example_topic_name, example_events)
        print(f"Successfully published batch with message IDs: {published_ids}")
    except Exception as e:
        print(f"Error publishing batch: {e}")
