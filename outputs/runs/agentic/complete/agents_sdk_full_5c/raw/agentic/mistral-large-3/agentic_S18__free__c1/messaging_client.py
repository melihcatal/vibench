import os
from google.cloud import pubsub_v1

def get_pubsub_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()

def get_pubsub_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()

def get_project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT")