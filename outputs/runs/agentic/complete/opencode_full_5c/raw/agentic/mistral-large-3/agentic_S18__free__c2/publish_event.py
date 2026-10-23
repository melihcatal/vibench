from google.cloud import pubsub_v1
import os
import json

# Provider: Google Cloud Pub/Sub
# Identifiable by: google.cloud.pubsub_v1, GOOGLE_APPLICATION_CREDENTIALS
publisher = pubsub_v1.PublisherClient()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC_NAME", "events-topic")


def publish_event(event_data: dict) -> str:
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    data = json.dumps(event_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id
