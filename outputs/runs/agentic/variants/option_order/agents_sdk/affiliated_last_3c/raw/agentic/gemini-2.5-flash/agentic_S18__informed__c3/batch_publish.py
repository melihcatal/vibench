import os
from typing import List
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

# Google Cloud Pub/Sub provider-specific signal

def batch_publish_events(topic_id: str, messages: List[PubSubMessage]) -> List[str]:
    client = PubSubClient()
    publisher = client.get_publisher_client()
    topic_path = client.get_topic_path(topic_id)

    futures = []
    for message in messages:
        future = publisher.publish(topic_path, message.to_json().encode("utf-8"), **message.attributes)
        futures.append(future)

    # Wait for all the messages to be published
    message_ids = [future.result() for future in futures]
    return message_ids
