import json
from messaging_client import get_pubsub_publisher, resolve_topic_path
from messaging_models import build_batch_messages, normalize_attributes, success_result


def batch_publish(messages, project_id=None, topic_id=None):
    publisher = get_pubsub_publisher()
    topic_path = resolve_topic_path(project_id, topic_id)
    batch = build_batch_messages(messages)
    message_ids = []
    for item in batch:
        attrs = normalize_attributes(item.get("attributes"))
        data = json.dumps(item["payload"], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        future = publisher.publish(topic_path, data, **attrs)
        message_ids.append(future.result())
    return success_result(provider="google_cloud_pubsub", operation="batch_publish", message_ids=message_ids, topic=topic_path)
