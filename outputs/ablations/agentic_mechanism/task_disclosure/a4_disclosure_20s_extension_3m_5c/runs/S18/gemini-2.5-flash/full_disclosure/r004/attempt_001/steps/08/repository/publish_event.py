
import json
from google.cloud import pubsub_v1

def publish_json_event(project_id: str, topic_id: str, event: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Encode the JSON event to bytes
    data = json.dumps(event).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage:
    # Replace with your Google Cloud Project ID and Topic ID
    # Ensure you have authenticated with `gcloud auth application-default login`
    # or set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    PROJECT_ID = "your-gcp-project-id"
    TOPIC_ID = "your-pubsub-topic-id"
    
    sample_event = {
        "timestamp": "2026-09-20T10:00:00Z",
        "sensor_id": "sensor-123",
        "temperature": 25.5,
        "unit": "celsius"
    }
    
    # publish_json_event(PROJECT_ID, TOPIC_ID, sample_event)
    print("To publish an event, uncomment the call to publish_json_event and provide your PROJECT_ID and TOPIC_ID.")
