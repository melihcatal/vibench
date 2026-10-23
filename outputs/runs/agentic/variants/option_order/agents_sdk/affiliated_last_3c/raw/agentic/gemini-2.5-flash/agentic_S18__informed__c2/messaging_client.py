import os
from google.cloud import pubsub_v1

# Environment variables for Google Cloud Pub/Sub:
# GOOGLE_CLOUD_PROJECT: Your GCP project ID
# GOOGLE_APPLICATION_CREDENTIALS: Path to your service account key file

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Returns a Google Cloud Pub/Sub PublisherClient instance."""
    # Client is created with credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or default ADC if running in GCP environment.
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Returns a Google Cloud Pub/Sub SubscriberClient instance."""
    # Client is created with credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or default ADC if running in GCP environment.
    return pubsub_v1.SubscriberClient()

# Example of how to ensure project ID is set
def get_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Environment variable GOOGLE_CLOUD_PROJECT must be set.")
    return project_id
