from __future__ import annotations

from typing import Any, Dict, Iterable, List
import os

import requests


def check_log_text_safety(
    texts: Iterable[str], requested_attributes: Dict[str, Dict[str, Any]] | None = None
) -> List[Dict[str, Any]]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    attributes = requested_attributes or {"TOXICITY": {}, "INSULT": {}, "THREAT": {}}
    results: List[Dict[str, Any]] = []
    for text in texts:
        response = requests.post(
            endpoint,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": attributes,
            },
            timeout=30,
        )
        response.raise_for_status()
        results.append(response.json())
    return results
