import os
import json
from typing import List
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_publisher_client
from messaging_models import BatchMessage


def publish_messages_batch(
    project_id: str, topic_id: str, messages: List[BatchMessage]
):
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []

    for message in messages:
        data = json.dumps(message.data).encode("utf-8")
        future = publisher.publish(topic_path, data, **message.attributes)
        futures.append(future)

    results = [future.result() for future in futures]
    return results
