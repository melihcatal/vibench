from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


DOCUMENT_AI_ENDPOINT = "https://us-documentai.googleapis.com/v1"


def get_google_access_token() -> str:
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ValueError("GOOGLE_OAUTH_ACCESS_TOKEN is required")
    return token


def get_document_ai_processor_path(processor_id: Optional[str] = None) -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("DOCUMENT_AI_LOCATION", "us")
    resolved_processor_id = processor_id or os.getenv("DOCUMENT_AI_PROCESSOR_ID")
    if not project_id or not resolved_processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT and DOCUMENT_AI_PROCESSOR_ID are required"
        )
    return (
        f"projects/{project_id}/locations/{location}/processors/{resolved_processor_id}"
    )


def document_ai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_google_access_token()}",
        "Content-Type": "application/json",
    }


def process_document(
    payload: Dict[str, Any], processor_id: Optional[str] = None
) -> Dict[str, Any]:
    processor_path = get_document_ai_processor_path(processor_id=processor_id)
    url = f"{DOCUMENT_AI_ENDPOINT}/{processor_path}:process"
    response = requests.post(
        url, headers=document_ai_headers(), json=payload, timeout=120
    )
    response.raise_for_status()
    return response.json()
