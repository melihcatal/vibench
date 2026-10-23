from google.cloud import pubsub_v1
import os
import json

def publish_json_event(project_id: str, topic_id: str, data: dict):
    """Publishes a JSON message to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    json_data = json.dumps(data)
    message_data = json_data.encode("utf-8")

    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, message_data)
    print(f"Published message ID: {future.result()}")
    return future.result()

if __name__ == "__main__":
    # Environment variables for demonstration
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "my-json-events-topic")

    event_payload = {
        "event_id": "12345",
        "type": "user_registered",
        "timestamp": "2023-10-27T10:00:00Z",
        "data": {
            "user_id": "user-abc-123",
            "email": "test@example.com"
        }
    }
    publish_json_event(PROJECT_ID, TOPIC_ID, event_payload)
