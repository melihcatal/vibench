from __future__ import annotations

import os
from typing import Dict, Sequence

from openai import OpenAI


MODEL = "gpt-4o-mini"


def archive_summary(segments: Sequence[str], max_sentences: int = 5) -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    transcript = "\n".join(segment.strip() for segment in segments if segment.strip())
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"Summarize the transcript for archival storage in no more than {max_sentences} sentences.",
            },
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return {
        "provider": "OpenAI",
        "model": MODEL,
        "summary": summary.strip(),
    }
