import json

from google.cloud import pubsub_v1

from messaging_client import get_pubsub_client, topic_path
from messaging_models import PublishRequest, normalize_message_payload


def publish_event(topic: str, payload, attributes=None) -> str:
    client = get_pubsub_client()
    request = PublishRequest(
        topic=topic,
        payload=normalize_message_payload(payload),
        attributes={str(k): str(v) for k, v in (attributes or {}).items()},
    )
    data = json.dumps(request.payload, separators=(",", ":")).encode("utf-8")
    future = client.publish(topic_path(request.topic), data, **request.attributes)
    return future.result()
