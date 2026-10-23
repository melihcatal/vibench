from google.cloud import pubsub_v1
import os


def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient."""
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient."""
    return pubsub_v1.SubscriberClient()


def get_project_id():
    """Returns the Google Cloud Project ID from environment variable."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_topic_path(project_id, topic_id):
    """Returns the fully qualified topic path."""
    return pubsub_v1.PublisherClient.topic_path(project_id, topic_id)


def get_subscription_path(project_id, subscription_id):
    """Returns the fully qualified subscription path."""
    return pubsub_v1.SubscriberClient.subscription_path(project_id, subscription_id)
