from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncIterator, Iterable, Optional

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

from speech_models import StreamingSpeechConfig, TranscriptSegment, normalize_transcript_text


@dataclass(slots=True)
class SpeechClientConfig:
    api_key: str
    model: str = "nova-2"
    language_code: str = "en-US"
    punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("DEEPGRAM_API_KEY", ""),
        model=os.environ.get("DEEPGRAM_MODEL", "nova-2"),
        language_code=os.environ.get("DEEPGRAM_LANGUAGE", "en-US"),
        punctuation=os.environ.get("DEEPGRAM_PUNCTUATION", "true").lower() == "true",
        interim_results=os.environ.get("DEEPGRAM_INTERIM_RESULTS", "true").lower() == "true",
        sample_rate_hz=int(os.environ.get("DEEPGRAM_SAMPLE_RATE_HZ", "16000")),
    )


class DeepgramStreamingSpeechClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None) -> None:
        self.config = config or load_speech_config()
        if not self.config.api_key:
            raise RuntimeError("DEEPGRAM_API_KEY is required for Deepgram Streaming API")
        self.client = DeepgramClient(self.config.api_key)

    def _options(self, language_code: Optional[str] = None, punctuation: Optional[bool] = None, interim_results: Optional[bool] = None) -> LiveOptions:
        return LiveOptions(
            model=self.config.model,
            language=language_code or self.config.language_code,
            smart_format=punctuation if punctuation is not None else self.config.punctuation,
            interim_results=interim_results if interim_results is not None else self.config.interim_results,
            encoding="linear16",
            sample_rate=self.config.sample_rate_hz,
            channels=1,
        )

    async def stream_audio(self, audio_chunks: AsyncIterator[bytes], language_code: Optional[str] = None, punctuation: Optional[bool] = None, interim_results: Optional[bool] = None) -> AsyncIterator[TranscriptSegment]:
        conn = self.client.listen.asyncwebsocket.v("1")
        stream = conn.start(self._options(language_code, punctuation, interim_results))

        async def sender() -> None:
            async for chunk in audio_chunks:
                await stream.send(chunk)
            await stream.finish()

        async def receiver() -> AsyncIterator[TranscriptSegment]:
            async for event in stream:
                if event.event != LiveTranscriptionEvents.Transcript:
                    continue
                alt = event.channel.alternatives[0]
                text = normalize_transcript_text(alt.transcript)
                if not text:
                    continue
                yield TranscriptSegment(
                    text=text,
                    is_final=bool(event.is_final),
                    confidence=getattr(alt, "confidence", None),
                    raw={"provider": "deepgram", "event": event.to_json()},
                )

        import asyncio

        sender_task = asyncio.create_task(sender())
        try:
            async for item in receiver():
                yield item
        finally:
            await sender_task


def create_client() -> DeepgramStreamingSpeechClient:
    return DeepgramStreamingSpeechClient()
