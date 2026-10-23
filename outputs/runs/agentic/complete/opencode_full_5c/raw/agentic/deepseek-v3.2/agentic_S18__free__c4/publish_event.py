import json
import os
from google.cloud import pubsub_v1
from datetime import datetime


def publish_event(event_data, topic_id=None):
    """Publish a JSON event to Google Cloud Pub/Sub topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if topic_id is None:
        topic_id = os.environ.get("PUBSUB_TOPIC_ID", "event-topic")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    if isinstance(event_data, dict):
        event_data["published_at"] = datetime.utcnow().isoformat()
        data = json.dumps(event_data).encode("utf-8")
    else:
        data = event_data.encode("utf-8") if isinstance(event_data, str) else event_data

    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return {
        "message_id": message_id,
        "topic": topic_path,
        "provider": "google-cloud-pubsub",
    }


if __name__ == "__main__":
    sample_event = {
        "event_type": "user_action",
        "user_id": "user_123",
        "action": "login",
        "timestamp": datetime.utcnow().isoformat(),
    }
    result = publish_event(sample_event)
    print(f"Published event: {result}")
