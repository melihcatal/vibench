import json
from google.cloud import pubsub_v1

def publish_json_event(project_id: str, topic_id: str, event_data: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    json_payload = json.dumps(event_data).encode("utf-8")

    try:
        future = publisher.publish(topic_path, json_payload)
        message_id = future.result()
        print(f"Published message ID: {message_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        publisher.api.transport.close()

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Pub/Sub Topic ID
    # For example:
    # PROJECT_ID = "your-gcp-project-id"
    # TOPIC_ID = "your-pubsub-topic-id"
    PROJECT_ID = "your-gcp-project-id"  # Placeholder
    TOPIC_ID = "your-pubsub-topic-id"    # Placeholder

    # Example event data
    example_event = {
        "event_type": "user_registered",
        "user_id": "12345",
        "timestamp": "2026-09-20T10:00:00Z",
        "details": {
            "email": "test@example.com",
            "marketing_opt_in": True
        }
    }

    publish_json_event(PROJECT_ID, TOPIC_ID, example_event)
