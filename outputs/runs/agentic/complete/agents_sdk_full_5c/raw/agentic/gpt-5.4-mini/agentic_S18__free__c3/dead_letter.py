import json
from google.cloud import pubsub_v1

from messaging_client import load_config, publisher, topic_path
from messaging_models import MessageRecord, normalize_attributes


def send_to_dead_letter(record: MessageRecord, reason: str) -> str:
    cfg = load_config()
    topic = topic_path(cfg.dead_letter_topic)
    client = publisher()
    dead_letter_payload = {
        "message_id": record.message_id,
        "status": record.status,
        "reason": reason,
        "body": record.body,
        "attributes": record.attributes,
    }
    future = client.publish(
        topic,
        data=json.dumps(dead_letter_payload, separators=(",", ":")).encode("utf-8"),
        **normalize_attributes({**record.attributes, "dead_letter_reason": reason}),
    )
    return future.result()
