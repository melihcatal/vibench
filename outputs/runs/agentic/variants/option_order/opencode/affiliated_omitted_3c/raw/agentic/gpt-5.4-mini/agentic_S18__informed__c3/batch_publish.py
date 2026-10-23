import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_publisher
from messaging_models import BatchPublishRequest, normalize_attributes


def batch_publish(messages, topic_path=None):
    config = get_pubsub_config()
    publisher = get_publisher(config)
    topic_path = topic_path or config.topic_path
    request = BatchPublishRequest(messages=messages)
    results = []
    for item in request.messages:
        attrs = normalize_attributes(item.get("attributes"))
        future = publisher.publish(topic_path, json.dumps(item.get("payload", {})).encode("utf-8"), **attrs)
        results.append({"message_id": future.result(), "id": item.get("id"), "attributes": attrs})
    return {"topic_path": topic_path, "results": results}
