from google.cloud import pubsub_v1
import os


def get_publisher_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, this usually points to a service account key file
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return pubsub_v1.SubscriberClient()


def get_project_id():
    # Replace with your Google Cloud Project ID or load from environment
    # It's common to use os.getenv("GOOGLE_CLOUD_PROJECT") or similar
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
