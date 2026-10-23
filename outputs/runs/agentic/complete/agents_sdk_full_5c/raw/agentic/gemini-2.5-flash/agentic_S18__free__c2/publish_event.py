from google.cloud import pubsub_v1
import os
import json

def publish_json_event(project_id: str, topic_id: str, event_data: dict) -> str:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data_str = json.dumps(event_data)
    data = data_str.encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "my-event-topic")
    event = {"message": "Hello, Pub/Sub!", "timestamp": "2023-10-27T10:00:00Z"}
    
    # print(f"Publishing event to {TOPIC_ID}...")
    # message_id = publish_json_event(PROJECT_ID, TOPIC_ID, event)
    # print(f"Published message with ID: {message_id}")
