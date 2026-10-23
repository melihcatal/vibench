import os
from google.cloud import pubsub_v1


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT_ID", ""))


def get_pubsub_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_name: str) -> str:
    return f"projects/{project_id}/topics/{topic_name}"


def subscription_path(project_id: str, subscription_name: str) -> str:
    return f"projects/{project_id}/subscriptions/{subscription_name}"


def dead_letter_topic_path(project_id: str, dead_letter_topic_name: str) -> str:
    return f"projects/{project_id}/topics/{dead_letter_topic_name}"


def load_topic_config() -> dict:
    return {
        "project_id": get_project_id(),
        "topic_name": os.environ.get("PUBSUB_TOPIC_NAME", "events-main"),
        "subscription_name": os.environ.get(
            "PUBSUB_SUBSCRIPTION_NAME", "events-main-sub"
        ),
        "dead_letter_topic_name": os.environ.get(
            "PUBSUB_DEAD_LETTER_TOPIC_NAME", "events-dead-letter"
        ),
        "dead_letter_subscription_name": os.environ.get(
            "PUBSUB_DEAD_LETTER_SUBSCRIPTION_NAME", "events-dead-letter-sub"
        ),
        "max_delivery_attempts": int(
            os.environ.get("PUBSUB_MAX_DELIVERY_ATTEMPTS", "5")
        ),
    }


def build_publish_request(event_data: bytes, attributes: dict | None = None) -> dict:
    attrs = attributes or {}
    if "event_type" not in attrs:
        attrs["event_type"] = "unknown"
    return {
        "data": event_data,
        "attributes": attrs,
    }
