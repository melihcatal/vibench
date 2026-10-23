import os
import json
from google.cloud import pubsub_v1


def load_config() -> dict:
    return {
        "project_id": os.environ.get("GOOGLE_PROJECT_ID", "default-project"),
        "topic_id": os.environ.get("GOOGLE_PUBSUB_TOPIC_ID", "events-topic"),
        "subscription_id": os.environ.get(
            "GOOGLE_PUBSUB_SUBSCRIPTION_ID", "events-subscription"
        ),
        "dlq_topic_id": os.environ.get("GOOGLE_PUBSUB_DLQ_TOPIC_ID", "events-dlq"),
        "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
    }


def create_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def create_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def build_topic_path(
    publisher: pubsub_v1.PublisherClient, project_id: str, topic_id: str
) -> str:
    return publisher.topic_path(project_id, topic_id)


def build_subscription_path(
    subscriber: pubsub_v1.SubscriberClient, project_id: str, subscription_id: str
) -> str:
    return subscriber.subscription_path(project_id, subscription_id)


def parse_message_data(raw_data: bytes) -> dict:
    return json.loads(raw_data.decode("utf-8"))


def format_publish_payload(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")


def build_message_attributes(**kwargs) -> dict:
    return {k: str(v) for k, v in kwargs.items() if v is not None}
