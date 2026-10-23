from typing import AsyncIterator

from openai import OpenAI

from speech_client import create_openai_client, load_speech_config
from speech_models import RecognitionEvent, StreamChunk, event_from_payload


async def stream_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[RecognitionEvent]:
    config = load_speech_config()
    client: OpenAI = create_openai_client(config)
    async for audio in source:
        result = client.audio.transcriptions.create(model=config.model, file=audio)  # type: ignore[arg-type]
        yield event_from_payload({"text": getattr(result, "text", ""), "is_final": False, "language": config.language})
