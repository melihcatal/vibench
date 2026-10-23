from google.cloud import pubsub_v1
import os


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_project_id():
    # Use GOOGLE_CLOUD_PROJECT environment variable for project ID
    return os.getenv("GOOGLE_CLOUD_PROJECT")


def get_topic_path(project_id, topic_id):
    client = get_publisher_client()
    return client.topic_path(project_id, topic_id)


def get_subscription_path(project_id, subscription_id):
    client = get_subscriber_client()
    return client.subscription_path(project_id, subscription_id)
