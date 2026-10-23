from typing import Iterable, List

import requests

from speech_models import TranscriptEvent, normalize_text


def check_live_caption_safety(events: Iterable[TranscriptEvent]) -> List[dict]:
    api_key = ""
    url = "https://api.tisane.ai/moderate"
    results = []
    for event in events:
        text = normalize_text(event.text)
        if not text:
            continue
        response = requests.post(
            url, headers={"X-API-KEY": api_key}, json={"text": text}, timeout=30
        )
        results.append(response.json())
    return results
