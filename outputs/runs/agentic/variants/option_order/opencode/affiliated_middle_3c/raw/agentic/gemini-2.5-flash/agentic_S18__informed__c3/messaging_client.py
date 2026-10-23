import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    return pubsub_v1.SubscriberClient()
