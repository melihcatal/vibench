from __future__ import annotations

import os
from typing import Iterable, Sequence

from openai import OpenAI


DEFAULT_MODEL = "gpt-4o-mini"


def archive_summary(segments: Sequence[str] | Iterable[str], title: str | None = None) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    transcript_text = "\n".join(segment for segment in segments if segment)
    prompt = (
        "Create a concise archival summary of the following transcript. "
        "Return plain text with a short overview and 3 bullet highlights.\n\n"
        f"Title: {title or 'Untitled transcript'}\n\n"
        f"Transcript:\n{transcript_text}"
    )
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "You summarize transcripts for archival storage."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return {
        "provider": "OpenAI",
        "model": DEFAULT_MODEL,
        "summary": response.choices[0].message.content or "",
    }
