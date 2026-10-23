from google.cloud import pubsub_v1
import os
import json

def publish_event(project_id: str, topic_id: str, message: dict):
    """Publishes a message to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    message_json = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, message_json)
    print(f"Published message ID: {future.result()}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable)
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "my-test-topic")
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_message = {"data": "Hello, Pub/Sub!", "event_type": "test_event"}
        publish_event(PROJECT_ID, TOPIC_ID, sample_message)
