from __future__ import annotations

import os
from typing import List

from anthropic import Anthropic

from speech_models import ArchiveSummary

ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def archive_summary(transcript_text: str) -> ArchiveSummary:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required")
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        messages=[
            {"role": "user", "content": f"Summarize this transcription result into a title, bullets, and a short summary:\n\n{transcript_text}"}
        ],
    )
    text = "".join(block.text for block in message.content if hasattr(block, "text"))
    bullets: List[str] = [line.strip("- ") for line in text.splitlines() if line.strip()]
    title = bullets[0] if bullets else "Transcript Summary"
    return ArchiveSummary(title=title, bullets=bullets[1:4], summary=text)
