from messaging_client import get_publisher, get_pubsub_topic_path
from messaging_models import normalize_batch_item, normalize_attrs
import json


def batch_publish(project_id, topic_id, items):
    client = get_publisher()
    topic_path = get_pubsub_topic_path(project_id, topic_id)
    results = []
    for item in items:
        normalized = normalize_batch_item(item)
        data = json.dumps(normalized["payload"], separators=(",", ":")).encode("utf-8")
        attrs = normalize_attrs(normalized.get("attributes"))
        future = client.publish(topic_path, data=data, **attrs)
        results.append({"message_id": future.result(), "item_id": normalized.get("id")})
    return {"topic": topic_path, "results": results}
