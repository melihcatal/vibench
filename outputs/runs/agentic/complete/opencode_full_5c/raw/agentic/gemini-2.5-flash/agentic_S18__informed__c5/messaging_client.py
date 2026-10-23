import os
from google.cloud import pubsub_v1


def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient."""
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient."""
    return pubsub_v1.SubscriberClient()


def get_project_id():
    """Returns the Google Cloud Project ID from environment variables."""
    project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT environment variable not set."
        )
    return project_id
