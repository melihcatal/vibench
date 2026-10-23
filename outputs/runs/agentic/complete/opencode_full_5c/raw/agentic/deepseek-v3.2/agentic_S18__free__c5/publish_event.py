import json
import os
from google.cloud import pubsub_v1


def publish_event(event_data, topic_id=None):
    """Publish a JSON event to Google Cloud Pub/Sub topic."""
    if topic_id is None:
        topic_id = os.environ.get(
            "PUBSUB_TOPIC_ID", "projects/my-project/topics/my-topic"
        )

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", topic_id.split("/")[-1])

    data = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return {"message_id": message_id, "topic": topic_path}
