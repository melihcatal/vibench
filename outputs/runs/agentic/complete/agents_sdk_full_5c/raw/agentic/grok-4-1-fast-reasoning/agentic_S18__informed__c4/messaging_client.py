import os
from google.cloud import pubsub_v1

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TOPIC_ID = os.getenv("TOPIC_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
DEAD_LETTER_TOPIC_ID = os.getenv("DEAD_LETTER_TOPIC_ID", "dead-letter-topic")

def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()

def get_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()

def get_topic_path() -> str:
    publisher = get_publisher()
    return publisher.topic_path(GOOGLE_CLOUD_PROJECT, TOPIC_ID)

def get_dead_letter_topic_path() -> str:
    publisher = get_publisher()
    return publisher.topic_path(GOOGLE_CLOUD_PROJECT, DEAD_LETTER_TOPIC_ID)

def get_subscription_path() -> str:
    subscriber = get_subscriber()
    return subscriber.subscription_path(GOOGLE_CLOUD_PROJECT, SUBSCRIPTION_ID)