import json
import os
from google.cloud import pubsub_v1

def publish_batch_events(project_id: str, topic_id: str, messages: list[dict]):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for i, msg in enumerate(messages):
        json_data = json.dumps(msg)
        message_data = json_data.encode("utf-8")
        
        # Example of adding an attribute (e.g., a batch item ID)
        attributes = {"batch_item_id": str(i)}
        
        future = publisher.publish(topic_path, message_data, **attributes)
        futures.append(future)

    for future in futures:
        print(f"Published message in batch with ID: {future.result()}")

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC_ID")

    if not project_id or not topic_id:
        print("Please set GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC_ID environment variables.")
    else:
        sample_messages = [
            {"event_type": "product_view", "product_id": "P001", "user_id": "U1"},
            {"event_type": "product_view", "product_id": "P002", "user_id": "U2"},
            {"event_type": "add_to_cart", "product_id": "P001", "user_id": "U1", "quantity": 1}
        ]
        publish_batch_events(project_id, topic_id, sample_messages)
