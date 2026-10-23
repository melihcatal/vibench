from __future__ import annotations

import os
from typing import Dict, List, Sequence

from openai import OpenAI

OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def archive_summary(segments: Sequence[Dict[str, str]], max_bullets: int = 5) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    transcript_text = "\n".join(segment.get("text", "") for segment in segments if segment.get("text"))
    prompt = (
        f"Summarize the following transcript for archival search in at most {max_bullets} bullet points, "
        "followed by a one-sentence abstract.\n\n"
        f"Transcript:\n{transcript_text}"
    )
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You create concise meeting archive summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content or ""
    return {
        "provider": "OpenAI",
        "model": OPENAI_SUMMARY_MODEL,
        "summary": content,
    }
