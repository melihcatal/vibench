import os
from typing import Any, Dict, Optional

import requests

from safety_models import normalize_text

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def load_api_key() -> str:
    return os.getenv("PERSPECTIVE_API_KEY", "")


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def perspective_params() -> Dict[str, str]:
    return {"key": load_api_key()}


def prepare_text_payload(text: Any, language: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "comment": {"text": normalize_text(text)},
        "requestedAttributes": {"TOXICITY": {}},
    }
    if language:
        payload["languages"] = [language]
    return payload


def post_perspective(payload: Dict[str, Any]) -> Dict[str, Any]:
    session = build_session()
    response = session.post(
        PERSPECTIVE_API_URL, params=perspective_params(), json=payload, timeout=30
    )
    response.raise_for_status()
    return response.json()
