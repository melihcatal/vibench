from typing import Iterable, List

import requests


def check_caption_safety(chunks: Iterable[str]) -> List[dict]:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    key = __import__("os").environ["PERSPECTIVE_API_KEY"]
    results = []
    for text in chunks:
        resp = requests.post(
            endpoint,
            params={"key": key},
            json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
            timeout=30,
        )
        resp.raise_for_status()
        results.append(resp.json())
    return results
