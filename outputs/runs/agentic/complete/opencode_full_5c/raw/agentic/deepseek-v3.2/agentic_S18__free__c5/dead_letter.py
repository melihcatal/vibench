import json
import os
from google.cloud import pubsub_v1


def dead_letter(message_data, error_reason, dead_letter_topic_id=None):
    """Send failed messages to Google Cloud Pub/Sub dead-letter topic."""
    if dead_letter_topic_id is None:
        dead_letter_topic_id = os.environ.get(
            "DEAD_LETTER_TOPIC_ID", "projects/my-project/topics/dead-letter-topic"
        )

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", dead_letter_topic_id.split("/")[-1])

    dead_letter_payload = {
        "original_message": message_data,
        "error_reason": error_reason,
        "timestamp": os.environ.get("TIMESTAMP", "2023-01-01T00:00:00Z"),
    }

    data = json.dumps(dead_letter_payload).encode("utf-8")

    future = publisher.publish(topic_path, data, error_reason=error_reason)
    message_id = future.result()

    return {"dead_letter_message_id": message_id, "topic": topic_path}
