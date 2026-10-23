from google.cloud import pubsub_v1
import messaging_client
from messaging_models import encode_event
from typing import Dict, Any, List, Optional

def batch_publish(events: List[Dict[str, Any]], ids: Optional[List[str]] = None) -> List[str]:
    topic_path_str = messaging_client.topic_path()
    publisher = pubsub_v1.PublisherClient()
    messages = []
    for i, event in enumerate(events):
        data = encode_event(event)
        attrs = {'batch_index': str(i)}
        if ids and i < len(ids):
            attrs['custom_id'] = ids[i]
        messages.append((data, attrs))
    api_futures = publisher.publish(topic_path_str, *messages)
    message_ids = [future.result() for future in api_futures]
    return message_ids