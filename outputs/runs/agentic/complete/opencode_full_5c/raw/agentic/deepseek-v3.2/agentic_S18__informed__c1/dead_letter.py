import os
import json
from google.cloud import pubsub_v1


def dead_letter(message_data, reason="processing_failed", dead_letter_topic_id=None):
    """Send failed messages to a dead-letter topic in Google Cloud Pub/Sub."""
    if dead_letter_topic_id is None:
        dead_letter_topic_id = os.getenv(
            "PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
        )

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    if isinstance(message_data, dict):
        message_data["dead_letter_reason"] = reason
        data = json.dumps(message_data).encode("utf-8")
    else:
        dead_letter_payload = {
            "original_message": str(message_data),
            "dead_letter_reason": reason,
        }
        data = json.dumps(dead_letter_payload).encode("utf-8")

    attributes = {"dead_letter_reason": reason, "source": "pubsub_dead_letter"}

    future = publisher.publish(topic_path, data, **attributes)
    message_id = future.result()

    return {"message_id": message_id, "dead_letter_topic": topic_path, "reason": reason}
