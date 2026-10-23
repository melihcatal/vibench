import os
from google.cloud import pubsub_v1

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Returns a Google Cloud Pub/Sub Publisher client."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Returns a Google Cloud Pub/Sub Subscriber client."""
    return pubsub_v1.SubscriberClient()

def get_gcp_project_id() -> str:
    """Returns the GCP Project ID from environment variables."""
    return os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")

def get_topic_path(topic_id: str) -> str:
    """Returns the fully qualified topic path."""
    project_id = get_gcp_project_id()
    return f"projects/{project_id}/topics/{topic_id}"

def get_subscription_path(subscription_id: str) -> str:
    """Returns the fully qualified subscription path."""
    project_id = get_gcp_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"

MAIN_TOPIC_ID = os.getenv("PUB_SUB_TOPIC_ID", "main-events")
DEAD_LETTER_TOPIC_ID = os.getenv("PUB_SUB_DEAD_LETTER_TOPIC_ID", "main-events-dlq")
MAIN_SUBSCRIPTION_ID = os.getenv("PUB_SUB_SUBSCRIPTION_ID", "main-events-sub")
