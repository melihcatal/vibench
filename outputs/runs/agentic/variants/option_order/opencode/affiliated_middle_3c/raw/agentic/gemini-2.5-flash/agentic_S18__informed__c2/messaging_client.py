import os
from google.cloud import pubsub_v1


def get_publisher_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return pubsub_v1.SubscriberClient()


def get_project_id():
    # Assumes GOOGLE_CLOUD_PROJECT environment variable is set or gcloud is configured
    return os.getenv("GOOGLE_CLOUD_PROJECT")


def get_topic_path(project_id: str, topic_id: str):
    return pubsub_v1.PublisherClient.topic_path(project_id, topic_id)


def get_subscription_path(project_id: str, subscription_id: str):
    return pubsub_v1.SubscriberClient.subscription_path(project_id, subscription_id)
