import os

from google.cloud import pubsub_v1

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
if not GOOGLE_CLOUD_PROJECT:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required.")

PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "events-topic")
PUBSUB_SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION", "events-sub")
DEAD_LETTER_TOPIC = os.getenv("DEAD_LETTER_TOPIC", "dead-letter-topic")


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_topic_path():
    publisher = get_publisher_client()
    return publisher.topic_path(GOOGLE_CLOUD_PROJECT, PUBSUB_TOPIC)


def get_dead_letter_path():
    publisher = get_publisher_client()
    return publisher.topic_path(GOOGLE_CLOUD_PROJECT, DEAD_LETTER_TOPIC)


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_subscription_path():
    subscriber = get_subscriber_client()
    return subscriber.subscription_path(GOOGLE_CLOUD_PROJECT, PUBSUB_SUBSCRIPTION)
