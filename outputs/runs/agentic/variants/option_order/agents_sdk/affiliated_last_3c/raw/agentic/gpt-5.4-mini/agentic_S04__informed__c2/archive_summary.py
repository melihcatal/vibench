from __future__ import annotations

from typing import Iterable

from openai import OpenAI


CLIENT = OpenAI()
MODEL = "gpt-4o-mini"


def archive_summary(transcript_text: str, key_segments: Iterable[str]) -> str:
    highlights = "\n".join(f"- {s}" for s in key_segments)
    response = CLIENT.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You write concise archival summaries for meeting transcripts."},
            {"role": "user", "content": f"Transcript:\n{transcript_text}\n\nHighlights:\n{highlights}\n\nWrite a short archive summary."},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
