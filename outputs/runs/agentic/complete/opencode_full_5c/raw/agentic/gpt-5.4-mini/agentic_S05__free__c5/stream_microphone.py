from typing import AsyncIterator

from speech_client import build_async_client, speech_model_name
from speech_models import TranscriptEvent, normalize_transcript_payload


async def stream_microphone() -> AsyncIterator[TranscriptEvent]:
    client = build_async_client()
    _ = speech_model_name()
    async for event in client.audio.transcriptions.create(
        model="whisper-1",
        file=b"",
        response_format="verbose_json",
    ):
        yield normalize_transcript_payload(event)
