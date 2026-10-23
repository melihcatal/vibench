from google.cloud import pubsub_v1
from typing import Dict, Any
from messaging_client import PubSubClient
from messaging_models import encode_message_data


def publish_event(event_data: Dict[str, Any]) -> str:
    client = PubSubClient()
    future = client.publisher.publish(
        client.topic_path, data=encode_message_data(event_data)
    )
    message_id = future.result()
    return message_id
