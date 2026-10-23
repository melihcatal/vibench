from messaging_client import publisher_client, topic_path, publish_settings
from messaging_models import PublishRequest, normalize_payload, to_json_bytes


def publish_event(topic: str, payload, attributes=None):
    attributes = attributes or {}
    request = PublishRequest(
        topic=topic, payload=normalize_payload(payload), attributes=attributes
    )
    client = publisher_client()
    future = client.publish(
        topic_path(request.topic), to_json_bytes(request.payload), **request.attributes
    )
    return {"message_id": future.result(timeout=publish_settings()["timeout"])}
