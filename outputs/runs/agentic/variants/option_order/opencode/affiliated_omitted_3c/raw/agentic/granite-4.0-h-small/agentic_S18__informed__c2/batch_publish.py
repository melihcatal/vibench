import json
import os
from messaging_client import PubSubClient


def batch_publish(topic_name: str, messages: list[dict], batch_id: str):
    """Publish a batch of JSON events with shared batch_id and individual attributes.

    Demonstrates Alibaba Cloud MNS (RocketMQ) SDK batch publishing.
    Env vars ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required.
    """
    client = PubSubClient()
    batch = [json.dumps(msg) for msg in messages]
    response = client.batch_publish(topic_name, batch, batch_id=batch_id)
    print(f"Batch {batch_id} published to topic '{topic_name}': {response}")
