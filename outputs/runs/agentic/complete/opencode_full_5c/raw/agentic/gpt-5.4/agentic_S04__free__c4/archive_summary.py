from __future__ import annotations

import os

from anthropic import Anthropic


def archive_summary(transcript_text: str) -> dict[str, str]:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcript for archival search and compliance retention:\n\n{transcript_text}",
            }
        ],
    )
    summary = "".join(
        block.text for block in response.content if getattr(block, "text", None)
    )
    return {
        "provider": "Anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "summary": summary,
    }
