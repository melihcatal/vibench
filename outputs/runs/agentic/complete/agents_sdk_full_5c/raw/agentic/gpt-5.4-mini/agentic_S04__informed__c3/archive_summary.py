from __future__ import annotations

from typing import List

from openai import OpenAI

ARCHIVE_MODEL = "gpt-4o-mini"


def archive_summary(transcript_segments: List[str]) -> str:
    client = OpenAI()
    transcript = "\n".join(transcript_segments)
    completion = client.chat.completions.create(
        model=ARCHIVE_MODEL,
        messages=[
            {"role": "system", "content": "Summarize transcription results for archival storage."},
            {"role": "user", "content": transcript},
        ],
    )
    return completion.choices[0].message.content or ""
