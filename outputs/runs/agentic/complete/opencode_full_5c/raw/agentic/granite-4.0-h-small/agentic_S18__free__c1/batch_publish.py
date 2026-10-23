import json
from messaging_client import MessagingClient


def batch_publish(topic_name: str, events: list[dict]) -> None:
    """Publish a batch of JSON events to a managed Pub/Sub topic.

    Uses Google Cloud Pub/Sub's batching API via the publisher client,
    which is identifiable by the library import `google.cloud.pubsub_v1.publisher.publisher_client`.
    """
    client = MessagingClient()
    # Fully qualified topic name
    full_topic = f"projects/{client.project_id}/topics/{topic_name}"
    # Build a list of Pub/Sub messages (data must be bytes)
    messages = [
        google.cloud.pubsub_v1.publisher.messages.PubsubMessage(
            data=json.dumps(event).encode("utf-8")
        )
        for event in events
    ]
    # Publish the batch (the client handles batching under the hood)
    client.publisher.publish(full_topic, *messages)
    print(f"Published batch of {len(events)} messages to {full_topic}")
