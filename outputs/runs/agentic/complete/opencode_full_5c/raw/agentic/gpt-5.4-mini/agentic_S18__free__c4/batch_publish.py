from messaging_client import publisher_client, topic_path, publish_settings
from messaging_models import (
    BatchPublishRequest,
    PublishRequest,
    normalize_payload,
    to_json_bytes,
)


def batch_publish(topic: str, messages):
    normalized = [
        PublishRequest(
            topic=topic,
            payload=normalize_payload(m.get("payload")),
            attributes={str(k): str(v) for k, v in (m.get("attributes") or {}).items()},
        )
        for m in messages
    ]
    request = BatchPublishRequest(topic=topic, messages=normalized)
    client = publisher_client()
    topic_ref = topic_path(request.topic)
    results = []
    for item in request.messages:
        future = client.publish(
            topic_ref, to_json_bytes(item.payload), **item.attributes
        )
        results.append(future.result(timeout=publish_settings()["timeout"]))
    return {"message_ids": results}
