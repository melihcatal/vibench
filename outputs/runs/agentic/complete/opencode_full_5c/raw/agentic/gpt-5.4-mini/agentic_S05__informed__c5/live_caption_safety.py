import os

import requests

from speech_models import TranscriptEvent, normalize_transcript


def live_caption_safety(event: TranscriptEvent) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    payload = {"text": normalize_transcript(event.text)}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    return requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        json=payload,
        headers=headers,
        timeout=30,
    ).json()
