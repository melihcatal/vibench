import os
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1

from messaging_models import normalize_payload, normalize_topic_name


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_name: str) -> str:
    return get_publisher().topic_path(project_id, normalize_topic_name(topic_name))


def subscription_path(project_id: str, subscription_name: str) -> str:
    return get_subscriber().subscription_path(project_id, subscription_name)


def encode_message(payload: Dict[str, Any]) -> bytes:
    import json

    return json.dumps(normalize_payload(payload), sort_keys=True).encode("utf-8")


def decode_message(data: bytes) -> Dict[str, Any]:
    import json

    return normalize_payload(json.loads(data.decode("utf-8")))


def to_attributes(attributes: Optional[Dict[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (attributes or {}).items()}
