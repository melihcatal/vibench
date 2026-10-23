import os
import json
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubsubMessage, PublishResponse
from typing import List


def batch_publish(topic_id: str, messages: List[PubsubMessage]) -> PublishResponse:
    """Publishes a batch of messages with IDs or attributes to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    topic_path = client.get_topic_path(topic_id)

    futures = []
    for message in messages:
        future = client.publisher.publish(
            topic_path, message.to_json().encode("utf-8"), **(message.attributes or {})
        )
        futures.append(future)

    message_ids = [future.result() for future in futures]
    return PublishResponse(message_ids=message_ids)
