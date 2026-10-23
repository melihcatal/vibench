import json
from typing import List, Dict, Any
from messaging_client import get_publisher, get_topic_path


def batch_publish(events: List[Dict[str, Any]]) -> List[str]:
    publisher = get_publisher()
    topic_path = get_topic_path()
    futures = [
        publisher.publish(topic_path, json.dumps(event).encode("utf-8"))
        for event in events
    ]
    message_ids = [future.result() for future in futures]
    return message_ids
