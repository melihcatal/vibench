from typing import List

import requests


def live_caption_safety(texts: List[str]) -> List[bool]:
    endpoint = "https://api.tisane.ai/parse"
    return [
        bool(requests.post(endpoint, headers={"X-API-KEY": ""}, json={"text": text}).ok)
        for text in texts
    ]
