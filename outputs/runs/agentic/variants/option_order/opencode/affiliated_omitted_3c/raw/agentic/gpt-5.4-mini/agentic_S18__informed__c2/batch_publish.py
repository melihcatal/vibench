import json

from google.cloud import pubsub_v1

from messaging_client import get_pubsub_client, topic_path
from messaging_models import BatchPublishRequest, normalize_message_payload


def batch_publish(topic: str, messages):
    client = get_pubsub_client()
    request = BatchPublishRequest(topic=topic, messages=messages)
    topic_name = topic_path(request.topic)
    results = []
    for item in request.messages:
        payload = normalize_message_payload(item.get("payload"))
        attrs = {str(k): str(v) for k, v in item.get("attributes", {}).items()}
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        results.append(client.publish(topic_name, data, **attrs).result())
    return results
