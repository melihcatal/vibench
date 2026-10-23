import json
from typing import Dict, Any

from messaging_client import topic_path, publisher
from messaging_models import serialize_event


def publish_event(event: Dict[str, Any], topic_name: str = "events-topic") -> str:
    topic_p = topic_path(topic_name)
    data = serialize_event(event)
    future = publisher.publish(topic_p, data)
    return future.result()
