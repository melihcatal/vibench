from __future__ import annotations

import os

from anthropic import Anthropic


ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def archive_summary(transcript_text: str) -> dict[str, str]:
    if not os.getenv(ANTHROPIC_API_KEY_ENV):
        raise RuntimeError(
            f"Missing required environment variable: {ANTHROPIC_API_KEY_ENV}"
        )
    client = Anthropic()
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcript for archival search and compliance records:\n\n{transcript_text}",
            }
        ],
    )
    summary = "".join(
        block.text
        for block in response.content
        if getattr(block, "type", None) == "text"
    ).strip()
    return {"summary": summary, "provider": "anthropic", "model": ANTHROPIC_MODEL}
