import os
import json
from messaging_client import PubSubClient


def batch_publish(topic_name, messages):
    """Publish a batch of messages to a Pub/Sub topic.

    Args:
        topic_name (str): Name of the Pub/Sub topic.
        messages (list[dict]): List of message payloads (each a dict).
    """
    client = PubSubClient()
    # Convert each dict to JSON string
    payloads = [json.dumps(msg) for msg in messages]
    # Provider-specific batch publish (Google Cloud Pub/Sub supports batch via publish)
    response = client.publish(topic_name, payloads)
    print(f"Batch published {len(payloads)} messages to {topic_name}: {response}")


if __name__ == "__main__":
    topic = os.getenv("PUBSUB_TOPIC")
    if not topic:
        raise RuntimeError("PUBSUB_TOPIC environment variable not set")
    batch = [
        {"id": "batch_1", "value": "First"},
        {"id": "batch_2", "value": "Second"},
        {"id": "batch_3", "value": "Third"},
    ]
    batch_publish(topic, batch)
