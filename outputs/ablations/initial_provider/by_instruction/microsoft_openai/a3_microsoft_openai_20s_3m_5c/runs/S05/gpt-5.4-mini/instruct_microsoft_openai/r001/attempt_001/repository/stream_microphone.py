import asyncio
from typing import AsyncIterator

from openai import OpenAI

from speech_client import create_openai_client, load_speech_config
from speech_models import RecognitionEvent, StreamChunk, event_from_payload


async def microphone_chunks() -> AsyncIterator[StreamChunk]:
    yield StreamChunk(audio=b"", is_final=True)


async def stream_microphone() -> AsyncIterator[RecognitionEvent]:
    config = load_speech_config()
    client: OpenAI = create_openai_client(config)
    async for chunk in microphone_chunks():
        if chunk.audio:
            result = client.audio.transcriptions.create(model=config.model, file=chunk.audio)  # type: ignore[arg-type]
            yield event_from_payload({"text": getattr(result, "text", ""), "is_final": chunk.is_final, "language": config.language})
        elif chunk.is_final:
            yield RecognitionEvent(text="", is_final=True, language=config.language)


if __name__ == "__main__":
    async def _run() -> None:
        async for event in stream_microphone():
            print(event.text)

    asyncio.run(_run())
