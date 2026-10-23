from google.cloud import pubsub_v1
import messaging_client
from messaging_models import encode_event
from typing import Dict, Any

def publish_event(event: Dict[str, Any]) -> str:
    topic_path_str = messaging_client.topic_path()
    publisher = pubsub_v1.PublisherClient()
    data = encode_event(event)
    api_future = publisher.publish(topic_path_str, data)
    message_id = api_future.result()
    return message_id