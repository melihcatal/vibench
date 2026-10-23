from __future__ import annotations

import os
from typing import Optional

from google.cloud import pubsub_v1


PUBSUB_PROJECT_ID_ENV = "GCP_PROJECT_ID"
PUBSUB_TOPIC_ENV = "GCP_PUBSUB_TOPIC"
PUBSUB_SUBSCRIPTION_ENV = "GCP_PUBSUB_SUBSCRIPTION"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "GCP_PUBSUB_DEAD_LETTER_TOPIC"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


class MessagingConfig:
    def __init__(self) -> None:
        self.project_id = os.getenv(PUBSUB_PROJECT_ID_ENV, "demo-project")
        self.topic_id = os.getenv(PUBSUB_TOPIC_ENV, "customer-events")
        self.subscription_id = os.getenv(PUBSUB_SUBSCRIPTION_ENV, "customer-events-sub")
        self.dead_letter_topic_id = os.getenv(PUBSUB_DEAD_LETTER_TOPIC_ENV, "customer-events-dead-letter")

    @property
    def topic_path(self) -> str:
        return f"projects/{self.project_id}/topics/{self.topic_id}"

    @property
    def subscription_path(self) -> str:
        return f"projects/{self.project_id}/subscriptions/{self.subscription_id}"

    @property
    def dead_letter_topic_path(self) -> str:
        return f"projects/{self.project_id}/topics/{self.dead_letter_topic_id}"


def get_config() -> MessagingConfig:
    return MessagingConfig()


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def build_ordering_key(customer_id: Optional[str]) -> str:
    return customer_id or "default-customer"
