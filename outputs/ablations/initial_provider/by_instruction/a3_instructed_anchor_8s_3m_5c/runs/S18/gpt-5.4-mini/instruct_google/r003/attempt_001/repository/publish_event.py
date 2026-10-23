from google.cloud import pubsub_v1

from messaging_client import encode_json, publisher_client, topic_path
from messaging_models import build_message_request


def publish_event(topic: str, payload, attributes=None):
    request = build_message_request(topic, payload, attributes)
    client = publisher_client()
    future = client.publish(topic_path(request.topic), encode_json(request.payload), **request.attributes)
    message_id = future.result()
    return {"provider": "google.pubsub_v1", "topic": topic_path(request.topic), "message_id": message_id}
