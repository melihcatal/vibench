import os
from messaging_client import PubSubClient
from messaging_models import EventMessage, BatchEventMessage
from typing import List


def publish_batch_events(topic_id: str, batch: BatchEventMessage):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    publisher = client.get_publisher_client()
    topic_path = publisher.topic_path(client.project_id, topic_id)

    futures = []
    for event in batch.messages:
        future = publisher.publish(
            topic_path, event.to_json(), **(event.attributes or {})
        )
        futures.append(future)

    message_ids = [f.result() for f in futures]
    print(
        f"Published batch of {len(message_ids)} messages to topic {topic_id}. Message IDs: {message_ids}"
    )
    return message_ids


if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Create a topic first, e.g., 'my-test-topic'
    # gcloud pubsub topics create my-test-topic

    topic_id = os.getenv("PUBSUB_TOPIC_ID", "my-test-topic")
    sample_batch = BatchEventMessage(
        messages=[
            EventMessage(
                id="batch-event-1", data={"operation": "add", "item": "apple"}
            ),
            EventMessage(
                id="batch-event-2",
                data={"operation": "remove", "item": "banana"},
                attributes={"priority": "high"},
            ),
            EventMessage(
                id="batch-event-3", data={"operation": "update", "item": "orange"}
            ),
        ]
    )
    publish_batch_events(topic_id, sample_batch)
