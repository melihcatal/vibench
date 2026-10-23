from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Optional

import websockets

from speech_models import StreamingChunk, StreamingConfig, normalize_transcript_event


@dataclass(slots=True)
class SpeechClientConfig:
    api_key: str
    region: str = "eastus"
    language: str = "en-US"
    endpoint: str = "wss://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        return cls(
            api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
            region=os.environ.get("AZURE_SPEECH_REGION", "eastus"),
            language=os.environ.get("AZURE_SPEECH_LANGUAGE", "en-US"),
        )


class AzureStreamingSpeechClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None) -> None:
        self.config = config or SpeechClientConfig.from_env()

    def _ws_uri(self, cfg: StreamingConfig) -> str:
        return (
            f"{self.config.endpoint}?language={cfg.language or self.config.language}"
            f"&format=detailed&profanity=masked"
        )

    async def stream(self, chunks: AsyncIterator[StreamingChunk], cfg: StreamingConfig) -> AsyncIterator[dict[str, Any]]:
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "X-ConnectionId": cfg.connection_id,
        }
        async with websockets.connect(self._ws_uri(cfg), extra_headers=headers, ping_interval=None) as ws:
            await ws.send(self._speech_start_message(cfg))
            async for chunk in chunks:
                await ws.send(chunk.audio)
                message = await ws.recv()
                event = normalize_transcript_event(message)
                if event:
                    yield event
            await ws.send(self._speech_end_message())
            while True:
                try:
                    message = await ws.recv()
                except Exception:
                    break
                event = normalize_transcript_event(message)
                if event:
                    yield event

    def _speech_start_message(self, cfg: StreamingConfig) -> str:
        return (
            "Path: speech.config\r\n"
            f"X-RequestId: {cfg.connection_id}\r\n"
            "Content-Type: application/json\r\n\r\n"
            f'{{"context":{{"system":{{"name":"streaming-stt"}},"os":{{"platform":"python"}},"speech":{{"language":"{cfg.language or self.config.language}"}}}}}}'
        )

    def _speech_end_message(self) -> str:
        return "Path: speech.end\r\n\r\n"


__all__ = ["AzureStreamingSpeechClient", "SpeechClientConfig"]
