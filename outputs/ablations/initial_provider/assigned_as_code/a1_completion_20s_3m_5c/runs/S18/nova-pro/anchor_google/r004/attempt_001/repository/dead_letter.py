from google.cloud import pubsub_v1

from messaging_client import get_pubsub_client


def dead_letter(message, config=None):
    config = config or {}
    client = get_pubsub_client(config["project_id"])
    topic = client.topic_path(config["project_id"], config["dead_letter_topic_id"])
    future = client.publish(topic, message.encode("utf-8"))
    try:
        return {"message_id": future.result(timeout=30)}
    finally:
        client.stop()