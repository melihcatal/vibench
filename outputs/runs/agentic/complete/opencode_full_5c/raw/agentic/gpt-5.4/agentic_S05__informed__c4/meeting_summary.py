from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI


class MeetingSummarizer:
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def summarize_chunks(self, transcript_chunks: Iterable[str]) -> str:
        transcript = "\n".join(
            chunk.strip() for chunk in transcript_chunks if chunk and chunk.strip()
        )
        if not transcript:
            return ""
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Summarize live meeting transcript chunks into concise action-oriented notes.",
                },
                {
                    "role": "user",
                    "content": transcript,
                },
            ],
        )
        return response.output_text
