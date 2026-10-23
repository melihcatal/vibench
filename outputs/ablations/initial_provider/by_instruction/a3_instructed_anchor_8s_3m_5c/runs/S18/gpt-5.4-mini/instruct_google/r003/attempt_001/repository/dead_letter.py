from messaging_client import encode_json, publisher_client, topic_path
from messaging_models import build_message_request


def dead_letter(topic: str, payload, attributes=None):
    request = build_message_request(topic, payload, attributes)
    client = publisher_client()
    message_id = client.publish(topic_path(request.topic), encode_json(request.payload), **request.attributes).result()
    return {"provider": "google.pubsub_v1", "dead_letter_topic": topic_path(request.topic), "message_id": message_id}
