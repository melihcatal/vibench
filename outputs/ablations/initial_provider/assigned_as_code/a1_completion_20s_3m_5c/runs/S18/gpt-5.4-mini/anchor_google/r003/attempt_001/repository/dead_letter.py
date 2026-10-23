from google.cloud import pubsub_v1

from messaging_client import load_config
from messaging_models import encode_json


def dead_letter(payload, config=None):
    config = load_config(config)
    client = pubsub_v1.PublisherClient()
    topic = client.topic_path(config["project_id"], config["dead_letter_topic_id"])
    future = client.publish(topic, encode_json(payload.get("event", payload)), source="dead-letter")
    try:
        return {"message_id": future.result(timeout=30)}
    finally:
        client.stop()
