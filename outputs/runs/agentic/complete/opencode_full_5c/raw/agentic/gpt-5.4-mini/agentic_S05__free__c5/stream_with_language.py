from typing import AsyncIterator

from speech_client import build_async_client
from speech_models import TranscriptEvent, normalize_transcript_payload


async def stream_with_language(
    language: str = "en", punctuation: bool = True
) -> AsyncIterator[TranscriptEvent]:
    client = build_async_client()
    async for event in client.audio.transcriptions.create(
        model="whisper-1",
        file=b"",
        response_format="verbose_json",
        language=language,
        prompt="Enable punctuation" if punctuation else "",
    ):
        yield normalize_transcript_payload(event)
