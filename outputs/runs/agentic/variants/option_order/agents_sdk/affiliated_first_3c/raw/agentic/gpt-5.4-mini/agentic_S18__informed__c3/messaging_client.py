from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1

from messaging_models import BatchPublishRequest, PublishRequest, MessageEnvelope, normalize_attributes


DEFAULT_PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"
DEFAULT_TOPIC_ENV = "PUBSUB_TOPIC"
DEFAULT_SUBSCRIPTION_ENV = "PUBSUB_SUBSCRIPTION"
DEFAULT_DEAD_LETTER_TOPIC_ENV = "PUBSUB_DEAD_LETTER_TOPIC"


class MessagingConfigError(ValueError):
    pass


@lru_cache(maxsize=1)
def get_project_id() -> str:
    project_id = os.getenv(DEFAULT_PROJECT_ID_ENV)
    if not project_id:
        raise MessagingConfigError(f"Missing {DEFAULT_PROJECT_ID_ENV}")
    return project_id


@lru_cache(maxsize=1)
def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: Optional[str] = None) -> str:
    name = topic or os.getenv(DEFAULT_TOPIC_ENV)
    if not name:
        raise MessagingConfigError(f"Missing topic name and {DEFAULT_TOPIC_ENV}")
    return get_publisher().topic_path(get_project_id(), name)


def subscription_path(subscription: Optional[str] = None) -> str:
    name = subscription or os.getenv(DEFAULT_SUBSCRIPTION_ENV)
    if not name:
        raise MessagingConfigError(f"Missing subscription name and {DEFAULT_SUBSCRIPTION_ENV}")
    return get_subscriber().subscription_path(get_project_id(), name)


def dead_letter_topic_path(topic: Optional[str] = None) -> str:
    name = topic or os.getenv(DEFAULT_DEAD_LETTER_TOPIC_ENV)
    if not name:
        raise MessagingConfigError(f"Missing dead-letter topic and {DEFAULT_DEAD_LETTER_TOPIC_ENV}")
    return get_publisher().topic_path(get_project_id(), name)


def publish_json(request: PublishRequest) -> str:
    publisher = get_publisher()
    path = topic_path(request.topic)
    data = MessageEnvelope(
        message_id=request.attributes.get("message_id", ""),
        payload=request.payload,
        attributes=normalize_attributes(request.attributes),
    ).to_json().encode("utf-8")
    future = publisher.publish(path, data, **normalize_attributes(request.attributes))
    return future.result()


def publish_batch(request: BatchPublishRequest) -> list[str]:
    publisher = get_publisher()
    path = topic_path(request.topic)
    futures = []
    for envelope in request.messages:
        futures.append(
            publisher.publish(
                path,
                envelope.to_json().encode("utf-8"),
                **normalize_attributes(envelope.attributes),
            )
        )
    return [f.result() for f in futures]
