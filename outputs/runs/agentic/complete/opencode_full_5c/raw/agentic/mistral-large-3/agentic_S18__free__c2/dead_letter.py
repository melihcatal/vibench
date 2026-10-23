from google.cloud import pubsub_v1
import os
import json

# Provider: Google Cloud Pub/Sub
# Identifiable by: google.cloud.pubsub_v1, GOOGLE_APPLICATION_CREDENTIALS
publisher = pubsub_v1.PublisherClient()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
DEAD_LETTER_TOPIC_NAME = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_NAME", "dead-letter-topic")


def dead_letter(message_data: dict, error_details: str) -> str:
    topic_path = publisher.topic_path(PROJECT_ID, DEAD_LETTER_TOPIC_NAME)
    message_data["error_details"] = error_details
    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id
