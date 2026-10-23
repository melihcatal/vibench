from __future__ import annotations

import os

import requests

from speech_models import CaptionChunk, join_caption_chunks


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
        self.key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    def check(self, chunks: list[CaptionChunk]) -> dict:
        text = join_caption_chunks(chunks)
        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
        response = requests.post(
            url,
            headers={"Ocp-Apim-Subscription-Key": self.key, "Content-Type": "application/json"},
            json={"text": text},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
