import json
import os
from google.cloud import pubsub_v1

def publish_json_event(project_id: str, topic_id: str, data: dict):
    """Publishes a JSON message to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    json_data = json.dumps(data)
    message_data = json_data.encode("utf-8")

    future = publisher.publish(topic_path, message_data)
    print(f"Published message ID: {future.result()}")

if __name__ == '__main__':
    # Environment variables are typically used for configuration in real applications
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC_ID")

    if not project_id or not topic_id:
        print("Please set GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC_ID environment variables.")
    else:
        sample_data = {"event_type": "user_signed_up", "user_id": "123", "timestamp": "2023-10-27T10:00:00Z"}
        publish_json_event(project_id, topic_id, sample_data)
