import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Optional

import httpx


@dataclass
class StreamingRecognitionConfig:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    model: str = "latest_long"


class GoogleCloudSpeechStreamingRecognizer:
    def __init__(self, api_key: Optional[str] = None, region: str = "us") -> None:
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GCP_API_KEY")
        self.region = region
        self.base_url = f"https://speech.googleapis.com/v1/speech:recognize"

    def _build_request(self, audio_content_b64: str, config: StreamingRecognitionConfig) -> dict[str, Any]:
        return {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": 16000,
                "languageCode": config.language_code,
                "enableAutomaticPunctuation": config.enable_automatic_punctuation,
                "model": config.model,
            },
            "audio": {"content": audio_content_b64},
        }

    async def recognize(self, audio_content_b64: str, config: Optional[StreamingRecognitionConfig] = None) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY or GCP_API_KEY is required")
        payload = self._build_request(audio_content_b64, config or StreamingRecognitionConfig())
        params = {"key": self.api_key}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.base_url, params=params, json=payload)
            response.raise_for_status()
            return response.json()

    async def recognize_stream(self, chunks: AsyncIterator[str], config: Optional[StreamingRecognitionConfig] = None) -> dict[str, Any]:
        collected: list[str] = []
        async for chunk in chunks:
            collected.append(chunk)
        return await self.recognize("".join(collected), config=config)
