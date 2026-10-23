import json

from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import create_message_payload

def dead_letter(message_payload, config=None):
    config = config or {}
    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_path(publisher, config["dead_letter_topic_id"])

    # Add an attribute to indicate it's a dead-letter message
    attributes = message_payload.get("attributes", {})
    attributes["dead_letter_reason"] = config.get("reason", "unknown_failure")
    attributes["original_message_id"] = message_payload.get("message_id", "n/a")

    # The actual event data is in message_payload["data"]
    message = create_message_payload(message_payload["data"], attributes)

    future = publisher.publish(dead_letter_topic_path, message["data"], **message["attributes"])
    try:
        return {"dead_letter_message_id": future.result(timeout=30)}
    finally:
        publisher.stop()
