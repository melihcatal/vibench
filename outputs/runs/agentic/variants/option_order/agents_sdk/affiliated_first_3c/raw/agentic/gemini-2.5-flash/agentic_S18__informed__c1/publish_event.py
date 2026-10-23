import json
import os
from google.cloud import pubsub_v1

def publish_json_event(project_id: str, topic_id: str, event_data: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = json.dumps(event_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
    return future.result()

if __name__ == "__main__":
    # For demonstration purposes, replace with your actual project and topic
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    TOPIC_ID = "my-sample-topic"
    sample_event = {"message": "Hello from Pub/Sub!", "timestamp": "2023-10-27T10:00:00Z"}

    if PROJECT_ID:
        publish_json_event(PROJECT_ID, TOPIC_ID, sample_event)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
