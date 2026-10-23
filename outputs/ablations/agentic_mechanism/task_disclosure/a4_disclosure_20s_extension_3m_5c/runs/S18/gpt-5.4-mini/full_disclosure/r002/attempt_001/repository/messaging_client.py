from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Mapping, Optional

import requests


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str = ""
    api_base_url: str = "https://pubsub.googleapis.com/v1"
    credentials_path: str = ""
    access_token: str = ""


def load_config(env: Mapping[str, str] = os.environ) -> MessagingConfig:
    project_id = env.get("GOOGLE_CLOUD_PROJECT", "").strip() or env.get("GCP_PROJECT", "").strip()
    topic_id = env.get("PUBSUB_TOPIC_ID", "").strip()
    subscription_id = env.get("PUBSUB_SUBSCRIPTION_ID", "").strip()
    api_base_url = env.get("PUBSUB_API_BASE_URL", "https://pubsub.googleapis.com/v1").rstrip("/")
    credentials_path = env.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    access_token = env.get("GOOGLE_OAUTH_ACCESS_TOKEN", "").strip()
    return MessagingConfig(
        project_id=project_id,
        topic_id=topic_id,
        subscription_id=subscription_id,
        api_base_url=api_base_url,
        credentials_path=credentials_path,
        access_token=access_token,
    )


def normalize_topic_name(project_id: str, topic_id: str) -> str:
    topic_id = topic_id.strip()
    if topic_id.startswith("projects/"):
        return topic_id
    return f"projects/{project_id}/topics/{topic_id}"


def normalize_subscription_name(project_id: str, subscription_id: str) -> str:
    subscription_id = subscription_id.strip()
    if subscription_id.startswith("projects/"):
        return subscription_id
    return f"projects/{project_id}/subscriptions/{subscription_id}"


def _load_access_token_from_file(credentials_path: str) -> str:
    if not credentials_path:
        return ""
    with open(credentials_path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    token = payload.get("access_token") or payload.get("token") or ""
    return str(token).strip()


@lru_cache(maxsize=1)
def get_access_token(credentials_path: str = "", env_token: str = "") -> str:
    if env_token:
        return env_token.strip()
    token = _load_access_token_from_file(credentials_path)
    if token:
        return token
    return os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN", "").strip()


def build_headers(content_type: str = "application/json", access_token: str = "") -> Dict[str, str]:
    token = access_token.strip() or get_access_token()
    headers = {"Content-Type": content_type}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def build_pubsub_client(config: Optional[MessagingConfig] = None) -> requests.Session:
    session = requests.Session()
    cfg = config or load_config()
    session.headers.update(build_headers(access_token=cfg.access_token))
    session.params = {"alt": "json"}
    session.base_url = cfg.api_base_url  # type: ignore[attr-defined]
    session.project_id = cfg.project_id  # type: ignore[attr-defined]
    session.topic_name = normalize_topic_name(cfg.project_id, cfg.topic_id) if cfg.project_id and cfg.topic_id else ""  # type: ignore[attr-defined]
    session.subscription_name = normalize_subscription_name(cfg.project_id, cfg.subscription_id) if cfg.project_id and cfg.subscription_id else ""  # type: ignore[attr-defined]
    return session


def make_topic_url(config: MessagingConfig) -> str:
    if not config.project_id or not config.topic_id:
        raise ValueError("project_id and topic_id are required")
    return f"{config.api_base_url}/" + normalize_topic_name(config.project_id, config.topic_id)


def make_subscription_url(config: MessagingConfig) -> str:
    if not config.project_id or not config.subscription_id:
        raise ValueError("project_id and subscription_id are required")
    return f"{config.api_base_url}/" + normalize_subscription_name(config.project_id, config.subscription_id)


def create_topic_request_body(labels: Optional[Mapping[str, str]] = None, kms_key_name: str = "") -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    if labels:
        body["labels"] = dict(labels)
    if kms_key_name:
        body["kmsKeyName"] = kms_key_name
    return body
