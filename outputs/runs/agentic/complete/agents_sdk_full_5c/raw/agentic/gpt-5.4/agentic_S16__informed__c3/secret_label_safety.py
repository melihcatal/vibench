from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

from security_client import get_secrets_manager_client, require_secret_id


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT")


def secret_label_safety(secret_id: str | None = None) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")

    sm_client = get_secrets_manager_client()
    resolved_secret_id = secret_id or require_secret_id("ROTATION_SECRET_ID")
    metadata = sm_client.describe_secret(SecretId=resolved_secret_id)
    label_text = " ".join(f"{k}:{v}" for k, v in (metadata.get("Tags") or [] and [(t.get('Key',''), t.get('Value','')) for t in metadata.get('Tags', [])]))
    note_text = metadata.get("Description", "")
    combined_text = f"{label_text}\n{note_text}".strip()

    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        json={
            "comment": {"text": combined_text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {
        name: data["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in data.get("attributeScores", {})
    }
    unsafe = any(value >= 0.7 for value in scores.values())
    return {
        "secret_id": resolved_secret_id,
        "analyzed_text": combined_text,
        "scores": scores,
        "unsafe": unsafe,
    }
