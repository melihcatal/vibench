from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests


PUBSUB_API_BASE = "https://pubsub.googleapis.com/v1"
MODERATE_API_BASE = "https://api.openai.com/v1"
TRANSLATE_API_BASE = "https://translation.googleapis.com/language/translate/v2"
FIRESTORE_API_BASE = "https://firestore.googleapis.com/v1"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def pubsub_config() -> Dict[str, str]:
    project_id = _required_env("GCP_PROJECT_ID")
    topic_id = _required_env("GCP_PUBSUB_TOPIC_ID")
    subscription_id = _required_env("GCP_PUBSUB_SUBSCRIPTION_ID")
    dead_letter_topic_id = os.getenv(
        "GCP_PUBSUB_DEAD_LETTER_TOPIC_ID", f"{topic_id}-dead-letter"
    )
    token = _required_env("GCP_ACCESS_TOKEN")
    return {
        "project_id": project_id,
        "topic_id": topic_id,
        "subscription_id": subscription_id,
        "dead_letter_topic_id": dead_letter_topic_id,
        "access_token": token,
    }


def topic_path(topic_id: Optional[str] = None) -> str:
    config = pubsub_config()
    resolved = topic_id or config["topic_id"]
    return f"projects/{config['project_id']}/topics/{resolved}"


def subscription_path(subscription_id: Optional[str] = None) -> str:
    config = pubsub_config()
    resolved = subscription_id or config["subscription_id"]
    return f"projects/{config['project_id']}/subscriptions/{resolved}"


def pubsub_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {pubsub_config()['access_token']}",
        "Content-Type": "application/json",
    }


def post_json(
    url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: int = 30
) -> Dict[str, Any]:
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    if not response.content:
        return {}
    return response.json()


def pubsub_post(path_suffix: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return post_json(f"{PUBSUB_API_BASE}/{path_suffix}", payload, pubsub_headers())


def openai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {_required_env('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }


def google_translate_params() -> Dict[str, str]:
    return {"key": _required_env("GOOGLE_TRANSLATE_API_KEY")}


def firestore_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {_required_env('GCP_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }


def firestore_document_path(collection_id: str, document_id: str) -> str:
    project_id = _required_env("GCP_PROJECT_ID")
    database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID", "(default)")
    return f"projects/{project_id}/databases/{database_id}/documents/{collection_id}/{document_id}"


def firestore_value(value: Any) -> Dict[str, Any]:
    if value is None:
        return {"nullValue": None}
    if isinstance(value, bool):
        return {"booleanValue": value}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"integerValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, str):
        return {"stringValue": value}
    if isinstance(value, dict):
        return {
            "mapValue": {
                "fields": {str(k): firestore_value(v) for k, v in value.items()}
            }
        }
    if isinstance(value, list):
        return {"arrayValue": {"values": [firestore_value(item) for item in value]}}
    return {"stringValue": json.dumps(value, separators=(",", ":"), ensure_ascii=False)}


def firestore_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {key: firestore_value(value) for key, value in payload.items()}
