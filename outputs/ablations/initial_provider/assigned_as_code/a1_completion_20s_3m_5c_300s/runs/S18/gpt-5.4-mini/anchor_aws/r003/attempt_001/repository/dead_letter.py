import json

from messaging_client import load_config, publisher_client


def dead_letter(payload, config=None):
    config = load_config(config)
    client = publisher_client(config)
    topic = config["dead_letter_topic"]
    message = json.dumps(payload)
    future = client.publish(topic, message.encode("utf-8"))
    return {"dead_letter_message_id": future.result()}
