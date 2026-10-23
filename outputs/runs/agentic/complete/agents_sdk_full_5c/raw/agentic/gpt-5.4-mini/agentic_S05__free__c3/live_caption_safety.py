from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionRecord, normalize_caption_chunks


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def assess(self, captions: list[CaptionRecord]) -> str:
        text = "\n".join(normalize_caption_chunks(captions))
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": "Classify whether transcript text contains unsafe content."},
                {"role": "user", "content": text},
            ],
        )
        return response.output_text
