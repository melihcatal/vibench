import json

from google.cloud import pubsub_v1

from messaging_client import create_publisher_client, load_pubsub_config, topic_path


def dead_letter(payload, config=None):
    config = load_pubsub_config(config)
    client = create_publisher_client()
    topic = topic_path(client, config["project_id"], config["dead_letter_topic_id"])
    body = json.dumps(payload.get("message", payload)).encode("utf-8")
    future = client.publish(topic, body, reason=str(payload.get("reason", "failed")))
    try:
        return {"message_id": future.result(timeout=30)}
    finally:
        client.stop()
