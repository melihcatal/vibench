import os
from google.cloud import pubsub_v1


def get_publisher_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return pubsub_v1.SubscriberClient()
