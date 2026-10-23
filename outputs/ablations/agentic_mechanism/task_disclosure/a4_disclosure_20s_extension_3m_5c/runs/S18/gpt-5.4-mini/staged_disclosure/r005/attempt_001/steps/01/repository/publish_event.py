import json
import os

from google.cloud import pubsub_v1


def publish_event(event):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC_ID"]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data=data, content_type="application/json")
    return future.result()
