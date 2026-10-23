from __future__ import annotations

from typing import Any, AsyncIterator

from speech_models import StreamingTranscriptEvent, normalize_whitespace


async def iter_transcript_events(connection: Any) -> AsyncIterator[StreamingTranscriptEvent]:
    async for event in connection:
        event_type = getattr(event, "type", None) or event.get("type")
        if event_type == "conversation.item.input_audio_transcription.delta":
            delta = getattr(event, "delta", None) or event.get("delta", "")
            if delta:
                yield StreamingTranscriptEvent(
                    text=normalize_whitespace(delta),
                    is_final=False,
                    raw=event.model_dump() if hasattr(event, "model_dump") else dict(event),
                )
        elif event_type == "conversation.item.input_audio_transcription.completed":
            transcript = getattr(event, "transcript", None) or event.get("transcript", "")
            if transcript:
                yield StreamingTranscriptEvent(
                    text=normalize_whitespace(transcript),
                    is_final=True,
                    raw=event.model_dump() if hasattr(event, "model_dump") else dict(event),
                )


def coalesce_partial_text(parts: list[str], incoming: str) -> str:
    parts.append(normalize_whitespace(incoming))
    return normalize_whitespace(" ".join(p for p in parts if p))
