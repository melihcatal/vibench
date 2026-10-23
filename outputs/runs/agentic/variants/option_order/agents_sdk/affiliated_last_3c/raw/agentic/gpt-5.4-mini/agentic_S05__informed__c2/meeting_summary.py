from __future__ import annotations

from typing import Iterable

from anthropic import Anthropic


ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"


def summarize_meeting_transcripts(chunks: Iterable[str]) -> str:
    client = Anthropic()
    transcript = "\n".join(chunk for chunk in chunks if chunk.strip())
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=512,
        temperature=0.2,
        messages=[
            {"role": "user", "content": f"Summarize this live meeting transcript:\n\n{transcript}"}
        ],
    )
    return message.content[0].text if message.content else ""
