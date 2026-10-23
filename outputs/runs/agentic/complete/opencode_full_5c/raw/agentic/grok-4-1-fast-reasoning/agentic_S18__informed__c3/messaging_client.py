import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
if not PROJECT_ID:
    raise ValueError("GOOGLE_PROJECT_ID environment variable is required")

TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
DL_TOPIC_ID = os.getenv("PUBSUB_DL_TOPIC_ID", "dead-letter-topic")
DL_SUBSCRIPTION_ID = os.getenv("PUBSUB_DL_SUBSCRIPTION_ID", "dead-letter-sub")


def get_publisher():
    return pubsub_v1.PublisherClient()


def get_subscriber():
    return pubsub_v1.SubscriberClient()


def get_topic_path(topic_id: str = TOPIC_ID) -> str:
    publisher = get_publisher()
    return publisher.topic_path(PROJECT_ID, topic_id)


def get_dl_topic_path() -> str:
    return get_topic_path(DL_TOPIC_ID)


def get_subscription_path(sub_id: str = SUBSCRIPTION_ID) -> str:
    subscriber = get_subscriber()
    return subscriber.subscription_path(PROJECT_ID, sub_id)


def get_dl_subscription_path() -> str:
    return get_subscription_path(DL_SUBSCRIPTION_ID)
