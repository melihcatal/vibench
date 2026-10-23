from google.cloud import pubsub_v1
import os


def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    return pubsub_v1.SubscriberClient()


def get_project_id():
    """Returns the Google Cloud Project ID from environment variable."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id
