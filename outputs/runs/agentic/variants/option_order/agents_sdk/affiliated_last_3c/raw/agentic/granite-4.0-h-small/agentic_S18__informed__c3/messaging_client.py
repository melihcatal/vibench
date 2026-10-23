import os
from google.cloud import pubsub_v1

def get_pubsub_client():
    """Return an authenticated Pub/Sub client.",
    # Project ID can be read from env or default credentials
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    return pubsub_v1.PublisherClient()  # credentials loaded via GOOGLE_APPLICATION_CREDENTIALS env
