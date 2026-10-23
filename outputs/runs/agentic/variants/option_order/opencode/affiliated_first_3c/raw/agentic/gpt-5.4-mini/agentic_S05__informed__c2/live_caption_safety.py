import os
from typing import Iterable, List

import requests

from speech_models import TranscriptEvent, normalize_transcript_text


def check_live_caption_safety(chunks: Iterable[TranscriptEvent]) -> List[dict]:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    payload = {
        "text": "\n".join(
            normalize_transcript_text(chunk.text)
            for chunk in chunks
            if normalize_transcript_text(chunk.text)
        )
    }
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01",
        headers={"api-key": key, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("categoriesAnalysis", [])
