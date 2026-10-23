import json
from messaging_client import get_pubsub_publisher, resolve_topic_path
from messaging_models import build_event_payload, normalize_attributes, success_result


def publish_event(payload=None, attributes=None, project_id=None, topic_id=None):
    publisher = get_pubsub_publisher()
    topic_path = resolve_topic_path(project_id, topic_id)
    event_payload = build_event_payload(payload)
    attr_map = normalize_attributes(attributes)
    data = json.dumps(event_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    future = publisher.publish(topic_path, data, **attr_map)
    message_id = future.result()
    return success_result(provider="google_cloud_pubsub", operation="publish_event", message_id=message_id, topic=topic_path)
