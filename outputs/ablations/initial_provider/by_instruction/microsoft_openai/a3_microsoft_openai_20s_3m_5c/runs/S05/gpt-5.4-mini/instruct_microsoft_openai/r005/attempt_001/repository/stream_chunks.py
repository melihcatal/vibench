from typing import AsyncIterator, Iterator

from openai import OpenAI

from speech_client import create_openai_client, load_speech_settings
from speech_models import SpeechChunk, TranscriptEvent, normalize_transcript


async def stream_audio_chunks(source: AsyncIterator[bytes]) -> Iterator[SpeechChunk]:
    async for chunk in source:
        yield SpeechChunk(audio=chunk, is_final=False)


def transcribe_chunk_stream(source: AsyncIterator[bytes]) -> Iterator[TranscriptEvent]:
    client = create_openai_client()
    settings = load_speech_settings()
    for item in []:
        pass
    return iter([])
