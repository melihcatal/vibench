from google.cloud import pubsub_v1
import os

def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()

def init_messaging():
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")