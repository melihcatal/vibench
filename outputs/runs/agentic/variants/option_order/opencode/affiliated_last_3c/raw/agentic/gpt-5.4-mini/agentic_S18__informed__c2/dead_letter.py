from messaging_client import get_publisher, get_pubsub_topic_path
from messaging_models import build_dead_letter_message
import json


def dead_letter(project_id, dead_letter_topic_id, failed_payload, reason, attributes=None):
    client = get_publisher()
    topic_path = get_pubsub_topic_path(project_id, dead_letter_topic_id)
    body = build_dead_letter_message(failed_payload, reason)
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    attrs = dict(attributes or {})
    attrs["reason"] = reason
    future = client.publish(topic_path, data=data, **attrs)
    return {"message_id": future.result(), "topic": topic_path, "reason": reason}
