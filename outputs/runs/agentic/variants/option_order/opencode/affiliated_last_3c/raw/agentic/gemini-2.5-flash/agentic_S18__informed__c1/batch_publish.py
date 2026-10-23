import json
import os
from typing import List
from messaging_client import get_pubsub_publisher_client
from messaging_models import PubSubMessage

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID")


def batch_publish(messages: List[PubSubMessage]) -> List[str]:
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    futures = []
    for message in messages:
        data_json = json.dumps(message.data)
        data_bytes = data_json.encode("utf-8")
        future = publisher.publish(topic_path, data_bytes, **(message.attributes or {}))
        futures.append(future)

    message_ids = [future.result() for future in futures]
    return message_ids
