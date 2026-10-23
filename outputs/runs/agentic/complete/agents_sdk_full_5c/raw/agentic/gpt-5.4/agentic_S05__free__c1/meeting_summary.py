from __future__ import annotations

from typing import Iterable

from openai import AsyncOpenAI

from speech_models import merge_transcript_chunks


async def summarize_meeting_chunks(
    transcript_chunks: Iterable[str],
    *,
    model: str = "gpt-4.1-mini",
) -> str:
    client = AsyncOpenAI()
    transcript = merge_transcript_chunks(transcript_chunks)
    response = await client.responses.create(
        model=model,
        input=(
            "Summarize this live meeting transcript into concise bullets with decisions, "
            "action items, and open questions.\n\n"
            f"Transcript: {transcript}"
        ),
    )
    return response.output_text.strip()
