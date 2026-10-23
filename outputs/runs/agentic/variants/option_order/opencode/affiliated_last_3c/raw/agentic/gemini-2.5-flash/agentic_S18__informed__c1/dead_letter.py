import json
import os
from messaging_client import get_pubsub_publisher_client
from messaging_models import PubSubMessage

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DEAD_LETTER_TOPIC_ID = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID")


def send_to_dead_letter(message: PubSubMessage, error_reason: str) -> str:
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(PROJECT_ID, DEAD_LETTER_TOPIC_ID)

    message.attributes = message.attributes or {}
    message.attributes["error_reason"] = error_reason

    data_json = json.dumps(message.data)
    data_bytes = data_json.encode("utf-8")

    future = publisher.publish(topic_path, data_bytes, **message.attributes)
    message_id = future.result()
    return message_id
