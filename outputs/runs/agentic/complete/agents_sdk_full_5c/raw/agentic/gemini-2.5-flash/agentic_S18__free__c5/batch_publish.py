from google.cloud import pubsub_v1
import os
import json

def publish_batch_events(project_id: str, topic_id: str, messages: list[dict]):
    """Publishes a batch of JSON events to a Pub/Sub topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The ID of the Pub/Sub topic.
        messages: A list of dictionaries, where each dictionary represents a message.
                  Each message dict should have 'data' (dict) and optionally 'attributes' (dict).
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for msg in messages:
        data = msg.get("data", {})
        attributes = msg.get("attributes", {})

        data_bytes = json.dumps(data).encode("utf-8")

        future = publisher.publish(topic_path, data_bytes, **attributes)
        futures.append(future)

    # Wait for all messages to be published and collect their IDs
    published_ids = []
    for future in futures:
        published_ids.append(future.result())

    print(f"Published batch of messages. IDs: {published_ids}")
    return published_ids

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    TOPIC_ID = "my-batch-events-topic" # Ensure this topic exists in your GCP project

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        batch_messages = [
            {"data": {"order_id": "O1", "item": "Laptop"}, "attributes": {"type": "new_order"}},
            {"data": {"order_id": "O2", "item": "Mouse"}, "attributes": {"type": "new_order", "priority": "high"}},
            {"data": {"order_id": "O3", "item": "Keyboard"}, "attributes": {"type": "new_order"}},
        ]
        publish_batch_events(PROJECT_ID, TOPIC_ID, batch_messages)
