from google.cloud import pubsub_v1
import os
import json

def publish_event(project_id: str, topic_id: str, message: dict) -> str:
    """Publishes a message to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    message_json = json.dumps(message).encode("utf-8")
    
    future = publisher.publish(topic_path, message_json)
    return future.result()

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    TOPIC_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID")

    if not PROJECT_ID or not TOPIC_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_TOPIC_ID environment variables.")
    else:
        test_message = {"event": "test_event", "data": "Hello, Pub/Sub!"}
        message_id = publish_event(PROJECT_ID, TOPIC_ID, test_message)
        print(f"Published message with ID: {message_id}")
