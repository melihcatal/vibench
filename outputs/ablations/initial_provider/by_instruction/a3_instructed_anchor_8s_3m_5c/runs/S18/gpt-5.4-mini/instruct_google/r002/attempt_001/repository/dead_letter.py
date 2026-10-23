import json

from messaging_client import load_config, publisher_client


def dead_letter(payload):
    config = load_config()
    client = publisher_client()
    topic = client.topic_path(config.project_id, config.dead_letter_topic_id or "")
    future = client.publish(topic, json.dumps(payload).encode("utf-8"), dead_letter="true")
    return {"message_id": future.result()}


if __name__ == "__main__":
    print(json.dumps(dead_letter({"failed": True, "provider": "google-pubsub"})))
