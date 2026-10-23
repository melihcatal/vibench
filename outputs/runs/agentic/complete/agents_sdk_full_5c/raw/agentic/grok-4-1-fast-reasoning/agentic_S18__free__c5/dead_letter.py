import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_messaging_config
from typing import Dict, Any

def send_to_dead_letter(failed_message: Dict[str, Any], dl_topic: str = None) -&gt; str:
    config = get_messaging_config()
    project_id = config['project_id']
    dl_topic = dl_topic or config['dl_topic']
    publisher = pubsub_v1.PublisherClient()
    dl_topic_path = publisher.topic_path(project_id, dl_topic)
    data = json.dumps(failed_message).encode('utf-8')
    future = publisher.publish(dl_topic_path, data)
    message_id = future.result()
    return message_id