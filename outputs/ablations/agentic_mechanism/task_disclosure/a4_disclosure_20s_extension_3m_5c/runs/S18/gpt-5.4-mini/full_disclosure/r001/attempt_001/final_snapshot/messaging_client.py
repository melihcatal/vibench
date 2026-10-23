import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from google.api_core.client_options import ClientOptions
from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingConfig:
    project_id: Optional[str]
    topic_id: Optional[str]
    subscription_id: Optional[str]
    endpoint: Optional[str]


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def load_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=_clean(os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")),
        topic_id=_clean(os.getenv("PUBSUB_TOPIC_ID") or os.getenv("PUBSUB_TOPIC")),
        subscription_id=_clean(os.getenv("PUBSUB_SUBSCRIPTION_ID") or os.getenv("PUBSUB_SUBSCRIPTION")),
        endpoint=_clean(os.getenv("PUBSUB_EMULATOR_HOST")),
    )


def resolve_project_id(project_id: Optional[str] = None) -> str:
    resolved = _clean(project_id) or load_config().project_id
    if not resolved:
        raise ValueError("Missing Google Cloud project id")
    return resolved


def resolve_topic_path(project_id: Optional[str] = None, topic_id: Optional[str] = None) -> str:
    cfg = load_config()
    resolved_project = resolve_project_id(project_id)
    resolved_topic = _clean(topic_id) or cfg.topic_id
    if not resolved_topic:
        raise ValueError("Missing Pub/Sub topic id")
    return pubsub_v1.PublisherClient().topic_path(resolved_project, resolved_topic)


def resolve_subscription_path(project_id: Optional[str] = None, subscription_id: Optional[str] = None) -> str:
    cfg = load_config()
    resolved_project = resolve_project_id(project_id)
    resolved_subscription = _clean(subscription_id) or cfg.subscription_id
    if not resolved_subscription:
        raise ValueError("Missing Pub/Sub subscription id")
    return pubsub_v1.SubscriberClient().subscription_path(resolved_project, resolved_subscription)


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    cfg = load_config()
    if cfg.endpoint:
        return pubsub_v1.PublisherClient(client_options=ClientOptions(api_endpoint=cfg.endpoint))
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    cfg = load_config()
    if cfg.endpoint:
        return pubsub_v1.SubscriberClient(client_options=ClientOptions(api_endpoint=cfg.endpoint))
    return pubsub_v1.SubscriberClient()


def build_attributes(**attributes: Any) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for key, value in attributes.items():
        if value is None:
            continue
        result[str(key)] = str(value)
    return result


def encode_message_data(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    import json

    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
