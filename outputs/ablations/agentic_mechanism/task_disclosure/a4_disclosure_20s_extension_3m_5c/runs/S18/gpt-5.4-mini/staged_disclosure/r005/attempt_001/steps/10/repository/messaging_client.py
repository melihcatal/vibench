import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class PubSubConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "PubSubConfig":
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("PUBSUB_PROJECT_ID")
        if not project_id:
            raise ValueError("Missing Pub/Sub project id: set GOOGLE_CLOUD_PROJECT or PUBSUB_PROJECT_ID")
        return cls(
            project_id=project_id,
            topic_id=os.getenv("PUBSUB_TOPIC_ID"),
            subscription_id=os.getenv("PUBSUB_SUBSCRIPTION_ID"),
        )


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_id: str) -> str:
    return get_publisher_client().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return get_subscriber_client().subscription_path(project_id, subscription_id)


def publish_message(project_id: str, topic_id: str, data: bytes, **attributes: str) -> str:
    publisher = get_publisher_client()
    topic = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic, data, **attributes)
    return future.result()


def pull_messages(project_id: str, subscription_id: str, max_messages: int = 1, return_immediately: bool = True):
    subscriber = get_subscriber_client()
    subscription = subscriber.subscription_path(project_id, subscription_id)
    request = {
        "subscription": subscription,
        "max_messages": max_messages,
    }
    if return_immediately:
        request["return_immediately"] = True
    return subscriber.pull(request=request)
