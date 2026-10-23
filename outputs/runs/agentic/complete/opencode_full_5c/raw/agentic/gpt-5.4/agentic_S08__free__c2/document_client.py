from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from document_models import DocumentSource


GOOGLE_DOCAI_ENDPOINT = "https://us-documentai.googleapis.com/v1"


def get_document_ai_config() -> Dict[str, str]:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = os.environ.get("DOCUMENTAI_LOCATION", "us")
    processor_id = os.environ["DOCUMENTAI_PROCESSOR_ID"]
    bearer_token = os.environ["GOOGLE_OAUTH_ACCESS_TOKEN"]
    return {
        "project_id": project_id,
        "location": location,
        "processor_id": processor_id,
        "bearer_token": bearer_token,
    }


def build_document_ai_url(processor_id: Optional[str] = None) -> str:
    cfg = get_document_ai_config()
    target_processor = processor_id or cfg["processor_id"]
    return (
        f"{GOOGLE_DOCAI_ENDPOINT}/projects/{cfg['project_id']}"
        f"/locations/{cfg['location']}/processors/{target_processor}:process"
    )


def build_document_payload(source: DocumentSource) -> Dict[str, Any]:
    return {
        "rawDocument": {
            "content": source.content_base64,
            "mimeType": source.mime_type,
        }
    }


def process_document(
    source: DocumentSource,
    processor_id: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> Dict[str, Any]:
    cfg = get_document_ai_config()
    url = build_document_ai_url(processor_id=processor_id)
    client = session or requests.Session()
    response = client.post(
        url,
        headers={
            "Authorization": f"Bearer {cfg['bearer_token']}",
            "Content-Type": "application/json",
        },
        json=build_document_payload(source),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_entity_text(entity: Dict[str, Any]) -> Optional[str]:
    normalized = entity.get("normalizedValue", {})
    text = normalized.get("text") or entity.get("mentionText")
    return text.strip() if isinstance(text, str) else text


def get_entity_confidence(entity: Dict[str, Any]) -> float:
    value = entity.get("confidence")
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
