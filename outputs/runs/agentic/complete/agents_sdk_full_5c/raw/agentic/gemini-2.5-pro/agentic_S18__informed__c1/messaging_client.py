import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """
    Returns an authenticated Google Cloud Pub/Sub PublisherClient.
    """
    try:
        return pubsub_v1.PublisherClient()
    except Exception as e:
        print(f"Failed to create PublisherClient: {e}")
        raise

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """
    Returns an authenticated Google Cloud Pub/Sub SubscriberClient.
    """
    try:
        return pubsub_v1.SubscriberClient()
    except Exception as e:
        print(f"Failed to create SubscriberClient: {e}")
        raise

def get_project_id() -> str:
    """
    Gets the Google Cloud project ID from environment variables.
    """
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set.")
    return project_id

def get_topic_path(topic_id: str) -> str:
    """
    Returns the full topic path for a given topic ID.
    """
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"

def get_subscription_path(subscription_id: str) -> str:
    """
    Returns the full subscription path for a given subscription ID.
    """
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"
