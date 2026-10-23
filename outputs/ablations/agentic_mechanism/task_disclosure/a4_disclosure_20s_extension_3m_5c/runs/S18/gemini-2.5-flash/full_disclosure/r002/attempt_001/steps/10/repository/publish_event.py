from google.cloud import pubsub_v1
import json

def publish_json_event(project_id: str, topic_id: str, message: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Encode the JSON message to bytes
    message_data = json.dumps(message).encode("utf-8")

    # Publish the message
    future = publisher.publish(topic_path, message_data)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage (replace with your actual project and topic IDs)
    PROJECT_ID = "your-gcp-project-id"
    TOPIC_ID = "your-pubsub-topic-id"
    
    event_payload = {
        "event_type": "user_created",
        "user_id": "12345",
        "timestamp": "2026-09-20T10:00:00Z",
        "data": {"name": "John Doe", "email": "john.doe@example.com"}
    }
    
    publish_json_event(PROJECT_ID, TOPIC_ID, event_payload)
