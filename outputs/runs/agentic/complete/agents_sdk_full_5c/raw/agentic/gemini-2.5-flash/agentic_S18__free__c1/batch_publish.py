from google.cloud import pubsub_v1
import os
import json

def publish_batch_events(project_id: str, topic_id: str, events: list[dict]):
    """Publishes a batch of JSON messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for i, event in enumerate(events):
        json_data = json.dumps(event)
        message_data = json_data.encode("utf-8")
        future = publisher.publish(topic_path, message_data, event_id=str(event.get("event_id", f"batch-event-{i}")))
        futures.append(future)

    print(f"Published {len(events)} messages. Waiting for results...")
    for i, future in enumerate(futures):
        try:
            message_id = future.result()
            print(f"Message {i+1} published with ID: {message_id}")
        except Exception as e:
            print(f"Error publishing message {i+1}: {e}")
    return [f.result() for f in futures]

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    TOPIC_ID = os.getenv("PUBSUB_BATCH_TOPIC_ID", "my-batch-events-topic")

    batch_of_events = [
        {
            "event_id": "batch-001",
            "type": "product_viewed",
            "timestamp": "2023-10-27T11:00:00Z",
            "data": {"product_id": "prod-A", "user_id": "user-1"}
        },
        {
            "event_id": "batch-002",
            "type": "product_added_to_cart",
            "timestamp": "2023-10-27T11:01:00Z",
            "data": {"product_id": "prod-B", "user_id": "user-1", "quantity": 1}
        },
        {
            "event_id": "batch-003",
            "type": "user_logged_in",
            "timestamp": "2023-10-27T11:02:00Z",
            "data": {"user_id": "user-2", "ip_address": "192.168.1.1"}
        },
    ]
    publish_batch_events(PROJECT_ID, TOPIC_ID, batch_of_events)
