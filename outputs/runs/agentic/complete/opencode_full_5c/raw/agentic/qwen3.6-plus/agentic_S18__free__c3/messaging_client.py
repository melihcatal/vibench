import os
from typing import Optional
from google.cloud import pubsub_v1


PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "default-project")
PUBSUB_TOPIC = os.environ.get("PUBSUB_TOPIC", "events-topic")
PUBSUB_SUBSCRIPTION = os.environ.get("PUBSUB_SUBSCRIPTION", "events-subscription")
DEAD_LETTER_TOPIC = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "dead-letter-topic")
PUBSUB_CREDENTIALS_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")


_publisher: Optional[pubsub_v1.PublisherClient] = None
_subscriber: Optional[pubsub_v1.SubscriberClient] = None


def get_publisher() -> pubsub_v1.PublisherClient:
    global _publisher
    if _publisher is None:
        _publisher = pubsub_v1.PublisherClient()
    return _publisher


def get_subscriber() -> pubsub_v1.SubscriberClient:
    global _subscriber
    if _subscriber is None:
        _subscriber = pubsub_v1.SubscriberClient()
    return _subscriber


def get_topic_path(topic_name: Optional[str] = None) -> str:
    topic = topic_name or PUBSUB_TOPIC
    return f"projects/{PROJECT_ID}/topics/{topic}"


def get_subscription_path(subscription_name: Optional[str] = None) -> str:
    sub = subscription_name or PUBSUB_SUBSCRIPTION
    return f"projects/{PROJECT_ID}/subscriptions/{sub}"


def get_dead_letter_topic_path(topic_name: Optional[str] = None) -> str:
    topic = topic_name or DEAD_LETTER_TOPIC
    return f"projects/{PROJECT_ID}/topics/{topic}"


def reset_clients():
    global _publisher, _subscriber
    _publisher = None
    _subscriber = None


def build_pubsub_attributes(attributes: dict) -> dict:
    return {str(k): str(v) for k, v in attributes.items() if v is not None}


def decode_message_data(message_data: bytes) -> dict:
    import json

    return json.loads(message_data.decode("utf-8"))
