import os
from google.cloud import pubsub_v1

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_publisher():
    return pubsub_v1.PublisherClient()


def get_subscriber():
    return pubsub_v1.SubscriberClient()
