
import os
from google.cloud import pubsub_v1

# Load configuration from environment variables
project_id = os.environ.get("GCP_PROJECT_ID")
topic_id = os.environ.get("GCP_PUBSUB_TOPIC_ID")
subscription_id = os.environ.get("GCP_PUBSUB_SUBSCRIPTION_ID")
dead_letter_topic_id = os.environ.get("GCP_PUBSUB_DEAD_LETTER_TOPIC_ID")

def get_publisher_client():
    """
    Creates and returns a Google Cloud Pub/Sub PublisherClient.
    
    Assumes Google Cloud authentication is configured (e.g., via GOOGLE_APPLICATION_CREDENTIALS).
    """
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """
    Creates and returns a Google Cloud Pub/Sub SubscriberClient.

    Assumes Google Cloud authentication is configured (e.g., via GOOGLE_APPLICATION_CREDENTIALS).
    """
    return pubsub_v1.SubscriberClient()
