from google.cloud import pubsub_v1
import datetime
from typing import Dict, Any
from messaging_client import PubSubClient
from messaging_models import encode_message_data


def send_to_dead_letter(event_data: Dict[str, Any], error_msg: str = "") -> str:
    dl_data = {
        "original_event": event_data,
        "error": error_msg,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }
    client = PubSubClient()
    future = client.publisher.publish(
        client.dead_letter_topic_path, data=encode_message_data(dl_data)
    )
    return future.result()
