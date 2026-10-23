"""
Local configuration and client utilities for Streaming Speech-to-Text.
Provides generic helpers for multiple providers.
"""

import os
import json
import asyncio
import aiohttp
from typing import Any, Dict, Generator, Callable, Optional

# Supported providers and their credential environment variables
PROVIDERS = {
    "ibm-watson": {
        "class": "WatsonSttClient",  # placeholder class name
        "url_env": "IBM_STT_URL",
        "key_env": "IBM_STT_APIKEY",
        "handshake": {"action": "start", "content-type": "audio/l16; rate=16000"},
    },
    "deepgram": {
        "class": "DeepgramClient",
        "key_env": "DEEPGRAM_API_KEY",
        "url": "https://api.deepgram.com/v1/listen",
    },
    "aws-transcribe": {
        "class": "AwsTranscribeClient",
        "key_env": "AWS_ACCESS_KEY_ID",
        "secret_env": "AWS_SECRET_ACCESS_KEY",
        "region_env": "AWS_REGION",
        "endpoint": "wss://{region}.transcribe.amazonaws.com",
        "handshake": {"action": "start", "format": "audio/l16; rate=16000"},
    },
}


class BaseSpeechClient:
    """Base class for speech-to-text streaming clients."""

    async def __aenter__(self) -> "BaseSpeechClient":
        self._connected = False
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def connect(self) -> None:
        raise NotImplementedError()

    async def send_audio(self, chunk: bytes) -> None:
        raise NotImplementedError()

    async def receive(self) -> Generator[Dict[str, Any], None, None]:
        raise NotImplementedError()

    async def close(self) -> None:
        raise NotImplementedError()


class WatsonSttClient(BaseSpeechClient):
    """IBM Watson Speech-to-Text WebSocket client."""

    def __init__(self):
        self._uri = os.getenv(PROVIDERS["ibm-watson"]["url_env"])
        self._key = os.getenv(PROVIDERS["ibm-watson"]["key_env"])
        self._ws: Optional[asyncio.AbstractServer] = None

    async def connect(self) -> None:
        self._ws = await asyncio.start_server(self._handle, self._uri)
        print("Watson STT WebSocket listening")

    async def send_audio(self, chunk: bytes) -> None:
        # Directly send chunk to connected client socket in real implementation
        pass

    async def receive(self) -> Generator[Dict[str, Any], None, None]:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._run())
            while True:
                yield await self._recv()

    async def close(self) -> None:
        if self._ws:
            self._ws.close()
            await self._ws.wait_closed()

    async def _handle(self, reader, writer):
        async for data in reader:
            # Process incoming Watson response (mocked here)
            msg = json.loads(data)
            writer.write(
                json.dumps(
                    {"results": [{"alternatives": [{"transcript": "mock"}]}]}
                ).encode()
            )

    async def _recv(self):
        # Mock receive logic
        return {"results": [{"alternatives": [{"transcript": "mock"}]}]}


class DeepgramClient(BaseSpeechClient):
    """Deepgram Streaming API client."""

    def __init__(self):
        self._api_key = os.getenv(PROVIDERS["deepgram"]["key_env"])
        self._url = PROVIDERS["deepgram"]["url"]

    async def connect(self) -> None:
        self._session = aiohttp.ClientSession()

    async def send_audio(self, chunk: bytes) -> None:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "audio/l16; rate=16000",
        }
        async with self._session.post(self._url, headers=headers, data=chunk) as resp:
            if resp.status != 200:
                raise RuntimeError("Deepgram request failed")

    async def receive(self) -> Generator[Dict[str, Any], None, None]:
        # Deepgram streams interim results in the same request body; simplified demo
        async with self._session.get(self._url, timeout=300) as resp:
            async for line in resp.content:
                line = line.decode("utf-8").strip()
                if line:
                    yield {"results": [{"alternatives": [{"transcript": line}]}]}

    async def close(self) -> None:
        await self._session.close()


class AwsTranscribeClient(BaseSpeechClient):
    """Amazon Transcribe Streaming WebSocket client (boto3 utilities)."""

    def __init__(self):
        self._access_key = os.getenv(PROVIDERS["aws-transcribe"]["key_env"])
        self._secret_key = os.getenv(PROVIDERS["aws-transcribe"]["secret_env"])
        self._region = os.getenv(PROVIDERS["aws-transcribe"]["region_env"], "us-east-1")
        self._endpoint = PROVIDERS["aws-transcribe"]["endpoint"].format(
            region=self._region
        )
        self._ws: Optional[asyncio.AbstractServer] = None

    async def connect(self):
        self._ws = await asyncio.start_server(self._handle, self._endpoint)
        print("AWS Transcribe WebSocket started")

    async def send_audio(self, chunk: bytes) -> None:
        # Placeholder for sending audio via established WebSocket connection
        pass

    async def receive(self) -> Generator[Dict[str, Any], None, None]:
        # Mock receive for demo
        yield {"results": [{"alternatives": [{"transcript": "aws sample"}]}]}


def get_client(provider: str) -> BaseSpeechClient:
    """
    Returns an instance of the appropriate client class.
    Raises ValueError if provider not supported.
    """
    cfg = PROVIDERS.get(provider)
    if not cfg:
        raise ValueError(f"Unsupported provider: {provider}")
    if cfg["class"] == "WatsonSttClient":
        return WatsonSttClient()
    if cfg["class"] == "DeepgramClient":
        return DeepgramClient()
    if cfg["class"] == "AwsTranscribeClient":
        return AwsTranscribeClient()
    raise NotImplementedError(f"Provider {provider} not implemented")


if __name__ == "__main__":
    # Demo usage
    async def demo():
        client = get_client("ibm-watson")
        async with client:
            await client.connect()
            await client.send_audio(b"audio_data...")
            async for result in client.receive():
                print("Result received:", result)

    asyncio.run(demo())
