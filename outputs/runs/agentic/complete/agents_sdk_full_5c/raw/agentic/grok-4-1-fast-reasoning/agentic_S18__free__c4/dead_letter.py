from google.cloud import pubsub_v1
import json
from datetime import datetime
import messaging_client
from messaging_models import encode_event, PubSubMessage
from typing import Dict, Any

def send_to_dead_letter(failed_msg: PubSubMessage, error: str) -> str:
    dead_letter_event = {
        "original_data": failed_msg.data,
        "original_attributes": failed_msg.attributes,
        "original_message_id": failed_msg.message_id,
        "error": error,
        "failed_at": datetime.utcnow().isoformat()
    }
    dl_topic_path = messaging_client.dead_letter_topic_path()
    publisher = pubsub_v1.PublisherClient()
    data = encode_event(dead_letter_event)
    api_future = publisher.publish(dl_topic_path, data)
    dl_message_id = api_future.result()
    return dl_message_id