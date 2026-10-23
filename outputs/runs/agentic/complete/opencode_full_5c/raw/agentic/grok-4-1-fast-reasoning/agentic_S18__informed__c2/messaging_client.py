import os
from google.cloud import pubsub_v1

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
PUBSUB_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
PUBSUB_DL_TOPIC_ID = os.getenv("PUBSUB_DL_TOPIC_ID", "dead-letter-topic")

_publisher_client = pubsub_v1.PublisherClient()
_subscriber_client = pubsub_v1.SubscriberClient()


def get_topic_path(topic_id: str = None) -> str:
    topic_id = topic_id or PUBSUB_TOPIC_ID
    return _publisher_client.topic_path(GOOGLE_CLOUD_PROJECT, topic_id)


def get_subscription_path(subscription_id: str = None) -> str:
    subscription_id = subscription_id or PUBSUB_SUBSCRIPTION_ID
    return _subscriber_client.subscription_path(GOOGLE_CLOUD_PROJECT, subscription_id)


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return _publisher_client


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return _subscriber_client
