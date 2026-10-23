from messaging_client import get_pubsub_topic_path, get_publisher
from messaging_models import build_event_message, normalize_attrs
import json


def publish_event(project_id, topic_id, payload, attributes=None, message_id=None):
    client = get_publisher()
    topic_path = get_pubsub_topic_path(project_id, topic_id)
    body = build_event_message(payload, message_id=message_id)
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    attrs = normalize_attrs(attributes)
    future = client.publish(topic_path, data=data, **attrs)
    return {"message_id": future.result(), "topic": topic_path}
