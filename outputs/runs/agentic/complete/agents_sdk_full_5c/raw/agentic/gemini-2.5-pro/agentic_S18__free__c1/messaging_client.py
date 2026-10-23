from google.cloud import pubsub_v1
import os
import json

def get_publisher_client():
    """Initializes and returns a Pub/Sub Publisher client."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Initializes and returns a Pub/Sub Subscriber client."""
    return pubsub_v1.SubscriberClient()

def get_gcp_project_id():
    """Gets the GCP Project ID from environment variables."""
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    return project_id

def get_topic_path(publisher_client: pubsub_v1.PublisherClient, topic_id: str):
    """Returns the full path for a Pub/Sub topic."""
    project_id = get_gcp_project_id()
    return publisher_client.topic_path(project_id, topic_id)

def get_subscription_path(subscriber_client: pubsub_v1.SubscriberClient, subscription_id: str):
    """Returns the full path for a Pub/Sub subscription."""
    project_id = get_gcp_project_id()
    return subscriber_client.subscription_path(project_id, subscription_id)
