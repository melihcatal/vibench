from __future__ import annotations

import os
from typing import Any, Dict

from anthropic import Anthropic

ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"



def archive_summary(transcript_text: str) -> Dict[str, Any]:
    api_key = os.getenv(ANTHROPIC_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Missing API key in {ANTHROPIC_API_KEY_ENV}")
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=400,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcript for archival notes with key decisions and action items:\n\n{transcript_text}",
            }
        ],
    )
    summary_text = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
    return {
        "provider": "Anthropic",
        "model": ANTHROPIC_MODEL,
        "summary": summary_text,
    }
