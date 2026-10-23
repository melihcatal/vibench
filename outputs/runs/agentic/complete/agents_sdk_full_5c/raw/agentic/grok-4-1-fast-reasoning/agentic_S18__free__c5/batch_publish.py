import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_messaging_config
from typing import List, Dict, Any

def batch_publish(events: List[Dict[str, Any]], topic: str = None) -&gt; List[str]:
    config = get_messaging_config()
    project_id = config['project_id']
    topic = topic or config['topic']
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic)
    
    messages = []
    for i, event in enumerate(events):
        data = json.dumps(event).encode('utf-8')
        attributes = {'batch_index': str(i)}
        messages.append((data, **attributes))
    
    api_futures = publisher.publish_messages(topic_path, messages)
    message_ids = [future.result() for future in api_futures]
    return message_ids