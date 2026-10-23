import json
from messaging_client import PubSubClient


def batch_publish(topic_id, messages):
    """Publish a batch of JSON events to a managed Pub/Sub topic.

    Args:
        topic_id (str): Topic identifier.
        messages (list[dict]): List of event payloads, each with optional IDs/attributes.
    """
    client = PubSubClient()  # Google Cloud Pub/Sub provider
    json_messages = [json.dumps(msg) for msg in messages]
    response = client.publish_batch(topic_id, json_messages)
    print(f"Batch publish to {topic_id}: {response}")
