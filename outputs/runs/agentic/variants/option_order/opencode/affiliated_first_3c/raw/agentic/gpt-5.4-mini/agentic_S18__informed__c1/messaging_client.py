import os
from dataclasses import dataclass


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str


def load_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=os.getenv(
            "GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", "demo-project")
        ),
        topic_id=os.getenv("PUBSUB_TOPIC_ID", "events-topic"),
        subscription_id=os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-subscription"),
        dead_letter_topic_id=os.getenv(
            "PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter"
        ),
    )


def topic_path(project_id: str, topic_id: str) -> str:
    return f"projects/{project_id}/topics/{topic_id}"


def subscription_path(project_id: str, subscription_id: str) -> str:
    return f"projects/{project_id}/subscriptions/{subscription_id}"


def normalize_attributes(attributes):
    return {str(k): str(v) for k, v in (attributes or {}).items()}
