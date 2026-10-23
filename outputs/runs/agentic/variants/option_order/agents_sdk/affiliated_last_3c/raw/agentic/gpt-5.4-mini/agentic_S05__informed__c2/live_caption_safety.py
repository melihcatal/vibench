from __future__ import annotations

from typing import Iterable, List

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_live_transcript_safety(text_chunks: Iterable[str]) -> List[dict]:
    api_key = __import__("os").environ["PERSPECTIVE_API_KEY"]
    findings: List[dict] = []
    for chunk in text_chunks:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": chunk},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
            },
            timeout=30,
        )
        response.raise_for_status()
        findings.append(response.json())
    return findings
