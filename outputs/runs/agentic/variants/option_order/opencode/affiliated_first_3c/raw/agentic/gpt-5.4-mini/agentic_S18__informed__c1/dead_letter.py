import json
from google.cloud import pubsub_v1
from messaging_client import load_config, topic_path, normalize_attributes
from messaging_models import to_json_bytes


def dead_letter(event: dict):
    config = load_config()
    client = pubsub_v1.PublisherClient()
    data = {"failed_event": event, "reason": event.get("reason", "processing_failed")}
    future = client.publish(
        topic_path(config.project_id, config.dead_letter_topic_id),
        to_json_bytes(data),
        **normalize_attributes(event.get("attributes")),
    )
    return {"dead_letter_message_id": future.result()}
