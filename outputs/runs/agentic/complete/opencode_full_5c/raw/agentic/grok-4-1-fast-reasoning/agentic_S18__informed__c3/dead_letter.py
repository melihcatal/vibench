import json
from typing import Dict, Any
from messaging_client import get_publisher, get_dl_topic_path


def send_to_dead_letter(event_data: Dict[str, Any]) -> str:
    publisher = get_publisher()
    topic_path = get_dl_topic_path()
    data_str = json.dumps(event_data)
    data = data_str.encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id
