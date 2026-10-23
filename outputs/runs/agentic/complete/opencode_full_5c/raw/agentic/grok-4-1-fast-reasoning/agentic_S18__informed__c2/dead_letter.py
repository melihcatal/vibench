import os
import json
from messaging_client import get_topic_path, get_publisher_client
from messaging_models import MessageEvent


def send_to_dead_letter(event: MessageEvent, dl_topic_id: str = None) -> str:
    dl_topic_id = dl_topic_id or os.getenv("PUBSUB_DL_TOPIC_ID", "dead-letter-topic")
    dl_topic_path = get_topic_path(dl_topic_id)
    publisher = get_publisher_client()
    data = json.dumps(event.payload).encode("utf-8")
    future = publisher.publish(dl_topic_path, data=data, **(event.attributes or {}))
    return future.result()
