from google.cloud import pubsub_v1
import os

def get_publisher_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    return pubsub_v1.SubscriberClient()

def get_project_id():
    # Assumes project ID is set in the environment or gcloud config
    # For simplicity, directly using an env var here.
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
