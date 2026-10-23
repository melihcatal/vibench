from __future__ import annotations

import base64
import os
from typing import Any, Dict, Iterable, List, Optional

import requests

from document_models import DocumentSource


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"
GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_AI_MODERATION_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"


def load_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def build_google_vision_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def build_google_query_params(
    api_key_env: str = "GOOGLE_CLOUD_API_KEY",
) -> Dict[str, str]:
    return {"key": load_required_env(api_key_env)}


def build_openai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {load_required_env('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }


def to_google_image(document: DocumentSource) -> Dict[str, str]:
    return {"content": base64.b64encode(document.content).decode("utf-8")}


def post_json(
    url: str,
    payload: Dict[str, Any],
    headers: Dict[str, str],
    params: Optional[Dict[str, str]] = None,
    timeout: float = 60.0,
) -> Dict[str, Any]:
    response = requests.post(
        url, json=payload, headers=headers, params=params, timeout=timeout
    )
    response.raise_for_status()
    return response.json()


def build_vision_requests(
    document: DocumentSource, features: Iterable[Dict[str, Any]]
) -> Dict[str, Any]:
    return {
        "requests": [
            {
                "image": to_google_image(document),
                "features": list(features),
                "imageContext": {"languageHints": ["en", "es", "fr"]},
            }
        ]
    }


def extract_full_text_annotation(response_json: Dict[str, Any]) -> Dict[str, Any]:
    responses: List[Dict[str, Any]] = response_json.get("responses", [])
    if not responses:
        return {}
    return responses[0].get("fullTextAnnotation", {})


def extract_response_entry(response_json: Dict[str, Any]) -> Dict[str, Any]:
    responses: List[Dict[str, Any]] = response_json.get("responses", [])
    return responses[0] if responses else {}
