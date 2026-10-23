import os
from google.cloud import pubsub_v1

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def publish_event(data):
    data = data.encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
