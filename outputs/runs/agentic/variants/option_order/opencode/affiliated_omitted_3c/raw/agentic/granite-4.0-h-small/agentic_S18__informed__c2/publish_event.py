import json
import os
from messaging_client import PubSubClient


def publish_event(topic_name: str, event_data: dict):
    """Publish a JSON event to a managed Pub/Sub topic.

    Uses Alibaba Cloud MNS (RocketMQ) SDK for demonstration.
    Requires environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET.
    """
    # Ensure event is a JSON string
    message = json.dumps(event_data)
    client = PubSubClient()
    response = client.publish(topic_name, message)
    print(f"Published event to topic '{topic_name}': {response}")
