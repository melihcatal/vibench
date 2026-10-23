import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any, AsyncIterable, AsyncIterator, Dict, Optional

import websockets

from speech_models import AudioChunk, SpeechConfig, TranscriptEvent, normalize_transcript_events


@dataclass
class StreamingSpeechClient:
    api_key: str
    region: str
    endpoint: str
    model: str = "speech-to-text"

    async def _connect(self) -> Any:
        url = f"wss://{self.region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US"
        return await websockets.connect(url, extra_headers={"Ocp-Apim-Subscription-Key": self.api_key})

    async def stream_chunks(self, chunks: AsyncIterable[AudioChunk], language_code: str = "en-US") -> AsyncIterator[TranscriptEvent]:
        ws = await self._connect()
        try:
            await ws.send(json.dumps({"type": "config", "language": language_code, "model": self.model}))
            async for chunk in chunks:
                await ws.send(chunk.audio)
                if chunk.is_final:
                    await ws.send(json.dumps({"type": "end"}))
            while True:
                message = await ws.recv()
                if isinstance(message, bytes):
                    continue
                data = json.loads(message)
                if data.get("type") in {"partial", "final"}:
                    yield TranscriptEvent(text=data.get("text", ""), is_partial=data.get("type") == "partial", confidence=data.get("confidence"))
                if data.get("type") == "end":
                    break
        finally:
            await ws.close()

    async def stream_microphone(self, sample_rate_hz: int = 16000, language_code: str = "en-US") -> AsyncIterator[TranscriptEvent]:
        async def mic_source() -> AsyncIterator[AudioChunk]:
            yield AudioChunk(audio=b"", is_final=True)
        async for event in self.stream_chunks(mic_source(), language_code=language_code):
            yield event

    async def stream_with_language(self, language_code: str = "en-US", enable_punctuation: bool = True) -> AsyncIterator[TranscriptEvent]:
        config = SpeechConfig(language_code=language_code, enable_punctuation=enable_punctuation)
        async def empty_chunks() -> AsyncIterator[AudioChunk]:
            yield AudioChunk(audio=b"", is_final=True)
        async for event in self.stream_chunks(empty_chunks(), language_code=config.language_code):
            yield event


def get_speech_client() -> StreamingSpeechClient:
    api_key = os.environ.get("AZURE_SPEECH_KEY", "")
    region = os.environ.get("AZURE_SPEECH_REGION", "eastus")
    endpoint = f"https://{region}.stt.speech.microsoft.com"
    return StreamingSpeechClient(api_key=api_key, region=region, endpoint=endpoint)
