import json
from messaging_client import get_pubsub_publisher, resolve_dead_letter_topic_path
from messaging_models import build_dead_letter_payload, normalize_attributes, success_result


def dead_letter(payload=None, attributes=None, project_id=None, dead_letter_topic_id=None):
    publisher = get_pubsub_publisher()
    topic_path = resolve_dead_letter_topic_path(project_id, dead_letter_topic_id)
    dlq_payload = build_dead_letter_payload(payload)
    attr_map = normalize_attributes(attributes)
    data = json.dumps(dlq_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    future = publisher.publish(topic_path, data, **attr_map)
    message_id = future.result()
    return success_result(provider="google_cloud_pubsub", operation="dead_letter", message_id=message_id, topic=topic_path)
