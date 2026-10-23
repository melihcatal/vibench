import os
from google.cloud import pubsub_v1

# Google Cloud Pub/Sub client creation helpers
# Provider is identified by the explicit import of google.cloud.pubsub_v1

def get_publisher_client():
    """Return an initialized PublisherClient with credentials from env vars."""
    project = os.getenv('GOOGLE_CLOUD_PROJECT')
    return pubsub_v1.PublisherClient()  # uses Application Default Credentials or service account file

def get_subscriber_client():
    """Return an initialized SubscriberClient with credentials from env vars."""
    return pubsub_v1.SubscriberClient()

# Optional: you could add logic to fall back to a service account JSON path here.
