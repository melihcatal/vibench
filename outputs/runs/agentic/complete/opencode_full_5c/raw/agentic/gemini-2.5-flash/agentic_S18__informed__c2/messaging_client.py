import os
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get(
    "GOOGLE_CLOUD_PROJECT"
)  # GOOGLE_CLOUD_PROJECT is often set from GOOGLE_APPLICATION_CREDENTIALS

if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_topic_path(topic_id: str):
    return f"projects/{PROJECT_ID}/topics/{topic_id}"


def get_subscription_path(subscription_id: str):
    return f"projects/{PROJECT_ID}/subscriptions/{subscription_id}"
