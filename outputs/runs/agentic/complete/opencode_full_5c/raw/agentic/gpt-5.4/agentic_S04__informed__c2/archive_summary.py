from __future__ import annotations

from typing import Iterable

from openai import OpenAI


def archive_summary(transcript_segments: Iterable[str]) -> str:
    client = OpenAI()
    content = "\n".join(transcript_segments)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize meeting transcripts for archival records in a concise paragraph.",
            },
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content or ""
