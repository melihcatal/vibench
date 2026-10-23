from __future__ import annotations

import os
from typing import Iterable

from openai import AsyncOpenAI

from speech_models import TranscriptChunk, collect_text


async def summarize_meeting_chunks(chunks: Iterable[TranscriptChunk]) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI summaries")
    transcript = collect_text(chunks)
    client = AsyncOpenAI(api_key=api_key)
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize live meeting transcript chunks into concise notes with decisions and action items.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
        "transcript": transcript,
    }
