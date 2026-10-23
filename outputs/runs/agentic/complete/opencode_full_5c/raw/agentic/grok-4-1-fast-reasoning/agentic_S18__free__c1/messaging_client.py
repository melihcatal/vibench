import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
if PROJECT_ID is None:
    raise ValueError("GCP_PROJECT_ID environment variable is required")

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()


def topic_path(topic_name: str) -> str:
    return publisher.topic_path(PROJECT_ID, topic_name)


def subscription_path(subscription_name: str) -> str:
    return subscriber.subscription_path(PROJECT_ID, subscription_name)
