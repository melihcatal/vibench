import os
from functools import lru_cache

from google.cloud import pubsub_v1


@lru_cache(maxsize=1)
def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT", ""))


@lru_cache(maxsize=1)
def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()
