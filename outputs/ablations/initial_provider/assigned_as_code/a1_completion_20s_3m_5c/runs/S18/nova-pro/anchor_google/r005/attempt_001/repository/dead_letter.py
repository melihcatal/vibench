import json

from google.cloud import pubsub_v1

def dead_letter(payload, config=None):
    config = config or {}
    client = pubsub_v1.PublisherClient()
    topic = client.topic_path(config["project_id"], config["dead_letter_topic_id"])
    future = client.publish(topic, json.dumps(payload["event"]).encode('utf-8'))
    try:
        return {'message_id': future.result(timeout=30)}
    finally:
        client.stop()