from __future__ import annotations

import os
from typing import Any, Dict, Iterable

import anthropic

ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
ANTHROPIC_MODEL = "claude-3-5-haiku-20241022"


def archive_summary(transcript_segments: Iterable[str]) -> Dict[str, Any]:
    api_key = os.getenv(ANTHROPIC_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {ANTHROPIC_API_KEY_ENV}")

    client = anthropic.Anthropic(api_key=api_key)
    content = "\n".join(segment for segment in transcript_segments if segment)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=300,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcript for long-term archive search and review:\n\n{content}",
            }
        ],
    )
    summary_text = "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
    return {
        "provider": "Anthropic",
        "model": ANTHROPIC_MODEL,
        "summary": summary_text,
    }
