
import os
from google.cloud import pubsub_v1

# Cache clients to avoid recreating them on every function call
_publisher_client = None
_subscriber_client = None

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """
    Provides a singleton instance of the Google Cloud Pub/Sub PublisherClient.
    
    Reads GCP configuration from environment variables.
    """
    global _publisher_client
    if _publisher_client is None:
        # For demonstration, we use default credentials from the environment
        # (e.g., by running `gcloud auth application-default login`)
        _publisher_client = pubsub_v1.PublisherClient()
    return _publisher_client

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """
    Provides a singleton instance of the Google Cloud Pub/Sub SubscriberClient.
    
    Reads GCP configuration from environment variables.
    """
    global _subscriber_client
    if _subscriber_client is None:
        _subscriber_client = pubsub_v1.SubscriberClient()
    return _subscriber_client

def load_configuration():
    """
    Loads and validates required environment variables for the messaging service.
    """
    required_vars = [
        "GCP_PROJECT_ID",
        "GCP_TOPIC_ID",
        "GCP_SUBSCRIPTION_ID",
        "GCP_DEAD_LETTER_TOPIC_ID"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Required environment variable '{var}' is not set.")
    print("Messaging client configuration loaded successfully.")

# You can call load_configuration() at module import time if you want to
# fail fast, or handle it within each function that needs the config.
# load_configuration()
