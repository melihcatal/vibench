from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from speech_models import CaptionChunk, SummaryResult, merge_caption_chunks


def summarize_meeting_chunks(chunks: Iterable[CaptionChunk], api_key: str | None = None) -> SummaryResult:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    transcript = merge_caption_chunks(chunks)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize meeting transcript chunks into concise notes with actions and decisions.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return SummaryResult(summary=response.output_text, raw=response.model_dump())
