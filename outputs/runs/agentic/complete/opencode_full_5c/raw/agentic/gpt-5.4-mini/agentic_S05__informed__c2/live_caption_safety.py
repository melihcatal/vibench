import os
from typing import Iterable, List

import requests


def live_caption_safety(chunks: Iterable[str]) -> List[dict]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = []
    for chunk in chunks:
        resp = requests.post(
            url,
            params={"key": api_key},
            json={"comment": {"text": chunk}, "requestedAttributes": {"TOXICITY": {}}},
            timeout=30,
        )
        resp.raise_for_status()
        results.append(resp.json())
    return results
