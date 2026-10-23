from google.cloud import pubsub_v1
import os
import json
from typing import List

# Provider: Google Cloud Pub/Sub
# Identifiable by: google.cloud.pubsub_v1, GOOGLE_APPLICATION_CREDENTIALS
publisher = pubsub_v1.PublisherClient()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC_NAME", "events-topic")


def batch_publish(messages: List[dict]) -> List[str]:
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    message_ids = []

    for message in messages:
        data = json.dumps(message).encode("utf-8")
        future = publisher.publish(topic_path, data)
        message_ids.append(future.result())

    return message_ids
