import os
import json
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubsubMessage, PublishResponse


def publish_event(topic_id: str, message: PubsubMessage) -> PublishResponse:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    topic_path = client.get_topic_path(topic_id)

    future = client.publisher.publish(
        topic_path, message.to_json().encode("utf-8"), **(message.attributes or {})
    )
    message_id = future.result()
    return PublishResponse(message_ids=[message_id])
