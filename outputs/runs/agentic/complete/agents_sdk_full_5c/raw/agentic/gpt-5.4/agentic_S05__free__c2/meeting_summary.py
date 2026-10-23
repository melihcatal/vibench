from __future__ import annotations

from typing import Iterable, Sequence

from openai import OpenAI

from speech_models import CaptionChunk, merge_transcript_text

OPENAI_MEETING_MODEL = "gpt-4o-mini"


def summarize_meeting_chunks(chunks: Sequence[CaptionChunk], api_key: str) -> str:
    client = OpenAI(api_key=api_key)
    transcript = merge_transcript_text(chunk.text for chunk in chunks)
    response = client.responses.create(
        model=OPENAI_MEETING_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize a live meeting transcript into concise bullets with decisions, risks, and action items.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return (response.output_text or "").strip()


def summarize_text_stream(chunks: Iterable[str], api_key: str) -> str:
    transcript = merge_transcript_text(chunks)
    return summarize_meeting_chunks([CaptionChunk(text=transcript)], api_key=api_key)
