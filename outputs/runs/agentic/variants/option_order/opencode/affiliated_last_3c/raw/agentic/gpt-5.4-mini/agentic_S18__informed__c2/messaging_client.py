import os
from google.cloud import pubsub_v1


DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("PUBSUB_PROJECT_ID")


def get_project_id():
    return DEFAULT_PROJECT


def get_publisher():
    return pubsub_v1.PublisherClient()


def get_subscriber():
    return pubsub_v1.SubscriberClient()


def get_pubsub_topic_path(project_id, topic_id):
    return f"projects/{project_id or DEFAULT_PROJECT}/topics/{topic_id}"


def get_subscription_path(project_id, subscription_id):
    return f"projects/{project_id or DEFAULT_PROJECT}/subscriptions/{subscription_id}"
