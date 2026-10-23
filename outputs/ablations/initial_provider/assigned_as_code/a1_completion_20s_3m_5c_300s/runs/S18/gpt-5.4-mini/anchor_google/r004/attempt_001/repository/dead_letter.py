import json

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path


def dead_letter(payload, config=None):
    config = load_config(config)
    client = publisher_client()
    topic = topic_path(client, config["project_id"], config["dead_letter_topic_id"])
    body = payload.get("message") if isinstance(payload, dict) else payload
    future = client.publish(topic, json.dumps(body).encode("utf-8"), reason=str(payload.get("reason", "failed")) if isinstance(payload, dict) else "failed")
    try:
        return {"dead_letter_message_id": future.result(timeout=30)}
    finally:
        client.stop()
