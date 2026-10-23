# batch_publish.py
# SAME-SCENARIO: publish multiple JSON messages to a Pub/Sub topic in a single batch request

import json
from google.cloud import pubsub_v1

def publish_batch(project_id: str, topic_id: str, messages: list[dict]):
    """Publish an iterable of JSON payloads to a Pub/Sub topic in a single batch call.

    Args:
        project_id: GCP project ID.
        topic_id: Pub/Sub topic name.
        messages: A list of JSON‑serializable dictionaries.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    # Convert each payload to a byte string
    data_items = [json.dumps(msg).encode('utf-8') for msg in messages]
    # publish() accepts an iterable of data items; it sends them as one batch
    message_ids = publisher.publish(topic_path, *data_items).result()
    print(f"Batch published {len(message_ids)} messages: {message_ids[:5]}...")

# Example usage (requires valid credentials and IDs)
# publish_batch(
#     "my-gcp-project",
#     "my-topic",
#     [{"event": "order_created", "order_id": 123},
#      {"event": "order_paid", "order_id": 123}]
# )
