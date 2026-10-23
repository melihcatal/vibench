import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_pubsub_topic_path
from messaging_models import BatchPublishRequest, normalize_payload

def batch_publish(messages, topic=None):
    publisher = get_publisher()
    topic_path = topic or get_pubsub_topic_path()
    request = BatchPublishRequest(messages=messages)
    futures = []
    for item in request.messages:
        payload = normalize_payload(item.get("payload"))
        attrs = dict(item.get("attributes") or {})
        futures.append(publisher.publish(topic_path, json.dumps(payload).encode("utf-8"), **attrs))
    return [future.result() for future in futures]
