from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptChunk


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def check(self, text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Classify whether the text contains unsafe content. Return a brief JSON-like judgment."},
                {"role": "user", "content": text},
            ],
        )
        verdict = response.choices[0].message.content or "unknown"
        return {"provider": "openai", "model": self.model, "verdict": verdict}


def check_live_transcript_safety(chunks: Iterable[TranscriptChunk]) -> List[dict]:
    checker = LiveCaptionSafetyChecker()
    return [checker.check(chunk.text) for chunk in chunks]
