from __future__ import annotations

from typing import Iterable

from anthropic import Anthropic

from speech_models import TranscriptWord


def archive_summary(segments: Iterable[TranscriptWord]) -> str:
    client = Anthropic()
    transcript_text = "\n".join(segment.text for segment in segments if segment.text)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize this transcription for archive:\n{transcript_text}"}],
    )
    return message.content[0].text if message.content else ""
