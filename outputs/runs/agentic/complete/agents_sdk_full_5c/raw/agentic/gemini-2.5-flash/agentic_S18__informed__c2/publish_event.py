from google.cloud import pubsub_v1
import json
import os

def publish_json_event(project_id: str, topic_id: str, data: dict):
    """Publishes a JSON event to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    json_data = json.dumps(data).encode("utf-8")

    try:
        future = publisher.publish(topic_path, json_data)
        message_id = future.result()
        print(f"Published message ID: {message_id}")
        return message_id
    except Exception as e:
        print(f"Error publishing message: {e}")
        raise

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    topic_id = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID_PUBLISH")
    event_data = {"message": "Hello, Pub/Sub!", "source": "publish_event.py"}

    if not all([project_id, topic_id]):
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_TOPIC_ID_PUBLISH environment variables.")
    else:
        publish_json_event(project_id, topic_id, event_data)
