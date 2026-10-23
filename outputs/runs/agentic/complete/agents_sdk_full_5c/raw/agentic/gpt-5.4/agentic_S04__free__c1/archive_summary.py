from __future__ import annotations

import os
from typing import Dict, Iterable, Optional

from openai import OpenAI

from speech_models import SummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def archive_summary(segments: Iterable[str], *, api_key: Optional[str] = None) -> Dict[str, object]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    joined = "\n".join(segment for segment in segments if segment)
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize the transcript for archival storage with key decisions, action items, and risks.",
            },
            {
                "role": "user",
                "content": joined,
            },
        ],
    )
    summary = SummaryResult(summary=response.output_text, model=OPENAI_SUMMARY_MODEL)
    return {
        "provider": "openai",
        "model": summary.model,
        "summary": summary.summary,
    }
