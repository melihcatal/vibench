from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def archive_summary(transcript_text: str, transcript_id: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize the transcript for archival search in 3 concise bullet points and one sentence overview.",
            },
            {
                "role": "user",
                "content": transcript_text,
            },
        ],
    )
    return {
        "provider": "OpenAI",
        "model": OPENAI_SUMMARY_MODEL,
        "transcript_id": transcript_id,
        "summary": response.output_text,
    }
