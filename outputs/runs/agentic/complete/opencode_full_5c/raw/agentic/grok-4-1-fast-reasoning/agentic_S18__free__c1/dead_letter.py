from typing import Dict, Any

from messaging_client import topic_path, publisher
from messaging_models import serialize_event


def send_to_dead_letter(
    failed_event: Dict[str, Any], dl_topic_name: str = "dead-letter-topic"
) -> str:
    topic_p = topic_path(dl_topic_name)
    data = serialize_event(failed_event)
    future = publisher.publish(topic_p, data, failed="true")
    return future.result()
