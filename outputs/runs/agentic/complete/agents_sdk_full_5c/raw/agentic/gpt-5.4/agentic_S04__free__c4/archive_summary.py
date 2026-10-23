from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from speech_models import SummaryResult

OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def archive_summary(transcript_segments: Iterable[str]) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    joined = "\n".join(transcript_segments)
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=(
            "Summarize this completed transcription for archival notes with key decisions and action items:\n\n"
            f"{joined}"
        ),
    )
    summary = SummaryResult(summary=response.output_text.strip(), model=OPENAI_SUMMARY_MODEL)
    return summary.__dict__
