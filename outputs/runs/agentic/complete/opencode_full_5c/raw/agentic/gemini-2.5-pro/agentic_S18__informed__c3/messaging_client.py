import os
from google.cloud import pubsub_v1


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_project_id():
    return os.environ["GOOGLE_CLOUD_PROJECT"]


def get_topic_path(topic_id):
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path(subscription_id):
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"
