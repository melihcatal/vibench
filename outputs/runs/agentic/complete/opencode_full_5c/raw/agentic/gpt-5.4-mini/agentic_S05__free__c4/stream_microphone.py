import asyncio
import os
from typing import AsyncIterator
import openai
from speech_client import build_client
from speech_models import TranscriptChunk, normalize_transcript_payload

async def stream_microphone() -> AsyncIterator[TranscriptChunk]:
    client = build_client()
    with open(os.getenv("MICROPHONE_AUDIO_PATH", "microphone.wav"), "rb") as audio:
        response = client.audio.transcriptions.create(
            model=os.getenv("OPENAI_STT_MODEL", "gpt-4o-mini-transcribe"),
            file=audio,
            response_format="verbose_json",
            language=os.getenv("SPEECH_LANGUAGE", "en"),
            temperature=0,
        )
    yield normalize_transcript_payload({"text": getattr(response, "text", ""), "final": True})

async def main() -> None:
    async for chunk in stream_microphone():
        print(chunk.text)

if __name__ == "__main__":
    asyncio.run(main())
