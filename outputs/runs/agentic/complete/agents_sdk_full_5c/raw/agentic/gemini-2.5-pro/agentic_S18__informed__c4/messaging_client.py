import os
from google.cloud import pubsub_v1

def get_publisher_client():
    """Returns a Google Cloud Pub/Sub Publisher client."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub Subscriber client."""
    return pubsub_v1.SubscriberClient()

def get_project_id():
    """Gets the Google Cloud project ID from environment variables."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id

def get_topic_path(publisher_client, project_id, topic_id):
    """Returns the full path for a Pub/Sub topic."""
    return publisher_client.topic_path(project_id, topic_id)

def get_subscription_path(subscriber_client, project_id, subscription_id):
    """Returns the full path for a Pub/Sub subscription."""
    return subscriber_client.subscription_path(project_id, subscription_id)

# Configuration
TOPIC_ID = os.getenv("GCP_PUBSUB_TOPIC_ID", "my-topic")
SUBSCRIPTION_ID = os.getenv("GCP_PUBSUB_SUBSCRIPTION_ID", "my-subscription")
DEAD_LETTER_TOPIC_ID = os.getenv("GCP_PUBSUB_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic")
