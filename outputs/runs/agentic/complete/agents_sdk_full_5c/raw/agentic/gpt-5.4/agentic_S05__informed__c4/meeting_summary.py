from __future__ import annotations

import os
from typing import Iterable

from anthropic import Anthropic

from speech_models import normalize_transcript_text


def summarize_meeting_transcript(
    transcript_chunks: Iterable[str],
    *,
    model: str = "claude-3-5-sonnet-20241022",
) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required")

    transcript = "\n".join(
        normalize_transcript_text(chunk) for chunk in transcript_chunks if normalize_transcript_text(chunk)
    )
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=500,
        system="You summarize live meeting transcripts into concise notes with decisions, action items, and risks.",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this meeting transcript:\n\n{transcript}",
            }
        ],
    )
    return "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    ).strip()
