from google.cloud import pubsub_v1
import os
import json

def publish_json_event(project_id: str, topic_id: str, data: dict, attributes: dict = None):
    """Publishes a JSON event to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data_bytes = json.dumps(data).encode("utf-8")

    if attributes is None:
        attributes = {}

    future = publisher.publish(topic_path, data_bytes, **attributes)
    print(f"Published message ID: {future.result()}")
    return future.result()

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    TOPIC_ID = "my-json-events-topic" # Ensure this topic exists in your GCP project

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        event_data = {"message": "Hello from publish_event.py!", "source": "python-app"}
        event_attributes = {"event_type": "greeting", "app_version": "1.0"}
        publish_json_event(PROJECT_ID, TOPIC_ID, event_data, event_attributes)
