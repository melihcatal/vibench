import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None
    credentials_file: Optional[str] = None
    endpoint: str = "pubsub.googleapis.com:443"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_config() -> MessagingConfig:
    project_id = _env("GOOGLE_CLOUD_PROJECT") or _env("GCLOUD_PROJECT") or _env("PUBSUB_PROJECT_ID")
    if not project_id:
        raise ValueError("Missing Google Cloud project id. Set GOOGLE_CLOUD_PROJECT or PUBSUB_PROJECT_ID.")
    return MessagingConfig(
        project_id=project_id,
        topic_id=_env("PUBSUB_TOPIC_ID"),
        subscription_id=_env("PUBSUB_SUBSCRIPTION_ID"),
        credentials_file=_env("GOOGLE_APPLICATION_CREDENTIALS"),
        endpoint=_env("PUBSUB_ENDPOINT", "pubsub.googleapis.com:443") or "pubsub.googleapis.com:443",
    )


@lru_cache(maxsize=1)
def get_config() -> MessagingConfig:
    return load_config()


def client_kwargs(config: Optional[MessagingConfig] = None) -> Dict[str, Any]:
    cfg = config or get_config()
    kwargs: Dict[str, Any] = {"client_options": {"api_endpoint": cfg.endpoint}}
    if cfg.credentials_file:
        kwargs["client_options"]["credentials_file"] = cfg.credentials_file
    return kwargs


def topic_path(topic_id: Optional[str] = None, config: Optional[MessagingConfig] = None) -> str:
    cfg = config or get_config()
    resolved = topic_id or cfg.topic_id
    if not resolved:
        raise ValueError("Missing topic id. Set PUBSUB_TOPIC_ID or pass topic_id.")
    return f"projects/{cfg.project_id}/topics/{resolved}"


def subscription_path(subscription_id: Optional[str] = None, config: Optional[MessagingConfig] = None) -> str:
    cfg = config or get_config()
    resolved = subscription_id or cfg.subscription_id
    if not resolved:
        raise ValueError("Missing subscription id. Set PUBSUB_SUBSCRIPTION_ID or pass subscription_id.")
    return f"projects/{cfg.project_id}/subscriptions/{resolved}"


def make_pubsub_client(config: Optional[MessagingConfig] = None):
    from google.cloud import pubsub_v1

    return pubsub_v1.PublisherClient(**client_kwargs(config))


def make_subscriber_client(config: Optional[MessagingConfig] = None):
    from google.cloud import pubsub_v1

    return pubsub_v1.SubscriberClient(**client_kwargs(config))
