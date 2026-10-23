from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import normalize_message_payload


def dead_letter(payload, config=None):
    config = config or {}
    project_id = config.get("project_id", get_project_id())
    dead_letter_topic_id = config["dead_letter_topic_id"]

    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_path(project_id, dead_letter_topic_id)

    data = normalize_message_payload(payload["event"])
    attributes = payload.get("attributes", {})

    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    try:
        return {"message_id": future.result(timeout=30)}
    finally:
        publisher.stop()
