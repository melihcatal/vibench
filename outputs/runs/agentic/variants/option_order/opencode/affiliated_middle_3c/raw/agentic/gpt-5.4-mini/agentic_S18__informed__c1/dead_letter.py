import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_dead_letter_topic_path
from messaging_models import DeadLetterRecord, normalize_payload

def dead_letter(payload, reason, original_message_id=None, topic=None):
    publisher = get_publisher()
    topic_path = topic or get_dead_letter_topic_path()
    record = DeadLetterRecord(payload=normalize_payload(payload), reason=reason, original_message_id=original_message_id)
    future = publisher.publish(topic_path, json.dumps(record.to_dict()).encode("utf-8"), reason=reason, original_message_id=original_message_id or "")
    return future.result()
