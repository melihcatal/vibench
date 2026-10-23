import os
from google.cloud import pubsub_v1

def get_publisher_client() -> tuple[pubsub_v1.PublisherClient, str]:
    """
    Creates a Pub/Sub Publisher client and gets the full topic path.
    
    Reads configuration from environment variables:
    - GCP_PROJECT_ID: The Google Cloud project ID.
    - GCP_TOPIC_ID: The Pub/Sub topic ID.
    """
    project_id = os.environ["GCP_PROJECT_ID"]
    topic_id = os.environ["GCP_TOPIC_ID"]
    
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_id)
    
    return client, topic_path

def get_subscriber_client() -> tuple[pubsub_v1.SubscriberClient, str]:
    """
    Creates a Pub/Sub Subscriber client and gets the full subscription path.
    
    Reads configuration from environment variables:
    - GCP_PROJECT_ID: The Google Cloud project ID.
    - GCP_SUBSCRIPTION_ID: The Pub/Sub subscription ID.
    """
    project_id = os.environ["GCP_PROJECT_ID"]
    subscription_id = os.environ["GCP_SUBSCRIPTION_ID"]
    
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project_id, subscription_id)
    
    return client, subscription_path
