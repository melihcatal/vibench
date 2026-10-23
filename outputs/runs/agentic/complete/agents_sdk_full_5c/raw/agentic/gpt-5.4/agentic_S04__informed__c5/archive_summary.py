from __future__ import annotations

import os
from typing import Dict, Iterable, List

from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def archive_summary(segments: Iterable[Dict[str, object]], max_sentences: int = 5) -> Dict[str, object]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=OPENAI_API_KEY)
    segment_list: List[Dict[str, object]] = list(segments)
    transcript_text = "\n".join(str(segment.get("text", "")) for segment in segment_list if segment.get("text"))
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": f"You summarize completed speech-to-text transcripts for archival storage in no more than {max_sentences} sentences.",
            },
            {
                "role": "user",
                "content": transcript_text,
            },
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return {
        "provider": "OpenAI Chat Completions",
        "model": OPENAI_MODEL,
        "summary": summary,
        "segment_count": len(segment_list),
    }
