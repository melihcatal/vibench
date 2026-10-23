import os
from google.cloud import pubsub_v1


def get_publisher_client():
    """Provides a Google Cloud Pub/Sub Publisher client."""
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    """Provides a Google Cloud Pub/Sub Subscriber client."""
    return pubsub_v1.SubscriberClient()


def get_project_id():
    """Gets the Google Cloud Project ID from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_topic_path(topic_id):
    """Returns the full path for a Pub/Sub topic."""
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path(subscription_id):
    """Returns the full path for a Pub/Sub subscription."""
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"
