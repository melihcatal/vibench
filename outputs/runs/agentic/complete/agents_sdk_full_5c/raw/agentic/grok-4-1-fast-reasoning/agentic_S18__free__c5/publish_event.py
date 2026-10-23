import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_messaging_config
from typing import Dict, Any

def publish_event(event: Dict[str, Any], topic: str = None) -&gt; str:
    config = get_messaging_config()
    project_id = config['project_id']
    topic = topic or config['topic']
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic)
    data = json.dumps(event).encode('utf-8')
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id