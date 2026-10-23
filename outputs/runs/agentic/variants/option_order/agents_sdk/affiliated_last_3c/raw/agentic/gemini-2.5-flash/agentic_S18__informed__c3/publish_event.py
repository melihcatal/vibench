import os
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

# Google Cloud Pub/Sub provider-specific signal

def publish_event(topic_id: str, message: PubSubMessage) -> str:
    client = PubSubClient()
    publisher = client.get_publisher_client()
    topic_path = client.get_topic_path(topic_id)

    future = publisher.publish(topic_path, message.to_json().encode("utf-8"), **message.attributes)
    message_id = future.result()
    return message_id
