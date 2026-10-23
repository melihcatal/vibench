from google.cloud import pubsub_v1
import os

def get_publisher_client():
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    return pubsub_v1.SubscriberClient()

def get_project_id():
    # Assumes GOOGLE_CLOUD_PROJECT or similar env var is set or credentials infer it.
    # For explicit setting: os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    return os.environ.get("GOOGLE_CLOUD_PROJECT")
