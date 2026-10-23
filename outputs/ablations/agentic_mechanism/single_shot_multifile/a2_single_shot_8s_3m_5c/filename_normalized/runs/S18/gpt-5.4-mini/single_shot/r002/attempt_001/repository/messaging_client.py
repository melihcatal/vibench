import os
from functools import lru_cache
from google.cloud import pubsub_v1


def _project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GCLOUD_PROJECT")


def get_pubsub_publisher():
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber():
    return pubsub_v1.SubscriberClient()


def resolve_topic_path(project_id=None, topic_id=None):
    project = project_id or _project_id()
    topic = topic_id or os.getenv("PUBSUB_TOPIC_ID")
    if not project or not topic:
        raise ValueError("project_id and topic_id are required")
    return f"projects/{project}/topics/{topic}"


def resolve_subscription_path(project_id=None, subscription_id=None):
    project = project_id or _project_id()
    subscription = subscription_id or os.getenv("PUBSUB_SUBSCRIPTION_ID")
    if not project or not subscription:
        raise ValueError("project_id and subscription_id are required")
    return f"projects/{project}/subscriptions/{subscription}"


def resolve_dead_letter_topic_path(project_id=None, dead_letter_topic_id=None):
    project = project_id or _project_id()
    topic = dead_letter_topic_id or os.getenv("PUBSUB_DLQ_TOPIC_ID")
    if not project or not topic:
        raise ValueError("project_id and dead_letter_topic_id are required")
    return f"projects/{project}/topics/{topic}"
