import json

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import MessageRequest


def publish_event(payload):
    config = load_config()
    client = publisher_client()
    topic = topic_path(config)
    request = MessageRequest(payload=payload)
    future = client.publish(topic, request.to_bytes(), **request.attributes)
    return {"message_id": future.result()}


if __name__ == "__main__":
    print(json.dumps(publish_event({"event": "created", "provider": "google-pubsub"})))
