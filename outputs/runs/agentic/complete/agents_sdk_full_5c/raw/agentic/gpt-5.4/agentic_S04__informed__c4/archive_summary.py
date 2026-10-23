from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from speech_models import SummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def archive_summary(transcript_segments: Iterable[str]) -> SummaryResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    joined_text = "\n".join(transcript_segments)
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Summarize the transcript for archival retrieval with key decisions, action items, and participants."},
            {"role": "user", "content": joined_text},
        ],
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(summary=summary, model=OPENAI_SUMMARY_MODEL, raw=response.model_dump())
