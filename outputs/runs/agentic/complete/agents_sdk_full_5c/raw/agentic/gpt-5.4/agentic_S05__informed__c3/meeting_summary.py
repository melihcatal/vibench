from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, SummaryResult, merge_caption_chunks


OPENAI_MODEL = "gpt-4o-mini"
OPENAI_ENV = "OPENAI_API_KEY"


def summarize_meeting_chunks(chunks: list[CaptionChunk]) -> SummaryResult:
    if not os.getenv(OPENAI_ENV):
        raise RuntimeError(f"Missing required environment variable: {OPENAI_ENV}")
    client = OpenAI()
    transcript = merge_caption_chunks(chunks)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript into concise action-oriented notes."},
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(summary=summary.strip(), raw=response)
