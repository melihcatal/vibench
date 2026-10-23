from google.cloud import pubsub_v1
import os

def get_publisher_client():
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    return pubsub_v1.SubscriberClient()

def get_project_id():
    # Replace with your Google Cloud Project ID or use environment variable
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")
