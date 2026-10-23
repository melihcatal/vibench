from __future__ import annotations

from typing import Dict, Iterable, List

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def archive_summary(transcript_segments: Iterable[str]) -> Dict[str, str]:
    client = OpenAI()
    joined = "\n".join(transcript_segments)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript for archival notes, decisions, and action items."},
            {"role": "user", "content": joined},
        ],
    )
    return {"summary": response.choices[0].message.content or ""}
