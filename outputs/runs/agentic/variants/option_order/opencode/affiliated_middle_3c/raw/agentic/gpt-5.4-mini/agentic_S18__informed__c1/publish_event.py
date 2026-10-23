import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_topic_path, get_publisher
from messaging_models import MessageEvent, normalize_payload, build_publish_result

def publish_event(payload, attributes=None, topic=None):
    client = get_publisher()
    topic_path = topic or get_pubsub_topic_path()
    event = MessageEvent(payload=normalize_payload(payload), attributes=attributes or {})
    future = client.publish(topic_path, json.dumps(event.payload).encode("utf-8"), **event.attributes)
    message_id = future.result()
    return build_publish_result(message_id=message_id, topic=topic_path, attributes=event.attributes)
