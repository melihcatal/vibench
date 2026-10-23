import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError


def get_publisher_client() -> pubsub_v1.PublisherClient:
    try:
        return pubsub_v1.PublisherClient()
    except GoogleAPICallError as e:
        print(f"Failed to create Pub/Sub publisher client: {e}")
        raise


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    try:
        return pubsub_v1.SubscriberClient()
    except GoogleAPICallError as e:
        print(f"Failed to create Pub/Sub subscriber client: {e}")
        raise


def get_project_id() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id


def get_topic_path(topic_id: str) -> str:
    return f"projects/{get_project_id()}/topics/{topic_id}"


def get_subscription_path(subscription_id: str) -> str:
    return f"projects/{get_project_id()}/subscriptions/{subscription_id}"
