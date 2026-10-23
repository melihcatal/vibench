from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Callable, Iterable, Iterator, Optional

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

from speech_models import AudioChunk, NormalizedTranscript, StreamingSpeechConfig, TranscriptSegment, normalize_text


@dataclass(slots=True)
class SpeechClientConfig:
    api_key: str
    model: str = "nova-2"
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("DEEPGRAM_API_KEY", ""),
        model=os.environ.get("DEEPGRAM_MODEL", "nova-2"),
        language_code=os.environ.get("DEEPGRAM_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.environ.get("DEEPGRAM_ENABLE_PUNCTUATION", "true").lower() == "true",
        interim_results=os.environ.get("DEEPGRAM_INTERIM_RESULTS", "true").lower() == "true",
    )


class DeepgramSpeechService:
    def __init__(self, config: Optional[SpeechClientConfig] = None) -> None:
        self.config = config or load_speech_config()
        self.client = DeepgramClient(self.config.api_key)

    def live_options(self, speech_config: Optional[StreamingSpeechConfig] = None) -> LiveOptions:
        cfg = speech_config or StreamingSpeechConfig()
        return LiveOptions(
            model=self.config.model,
            language=cfg.language_code or self.config.language_code,
            punctuate=cfg.enable_punctuation if speech_config else self.config.enable_punctuation,
            interim_results=cfg.interim_results if speech_config else self.config.interim_results,
            smart_format=True,
            sample_rate=cfg.sample_rate_hz,
            channels=cfg.channels,
        )

    def normalize_segment(self, payload: Any) -> NormalizedTranscript:
        channel = payload.channel.alternatives[0]
        transcript = normalize_text(channel.transcript)
        return NormalizedTranscript(
            text=transcript,
            final=bool(payload.is_final),
            language_code=getattr(payload, "language", None),
            confidence=getattr(channel, "confidence", None),
            raw={"type": "deepgram", "payload": payload},
        )

    def stream_from_iterable(self, chunks: Iterable[AudioChunk], speech_config: Optional[StreamingSpeechConfig] = None) -> Iterator[TranscriptSegment]:
        raise NotImplementedError("Wire this to Deepgram live transcription in a runtime integration.")

    async def stream_from_async_iterable(
        self,
        chunks: AsyncIterator[AudioChunk],
        speech_config: Optional[StreamingSpeechConfig] = None,
        on_segment: Optional[Callable[[TranscriptSegment], None]] = None,
    ) -> None:
        raise NotImplementedError("Wire this to Deepgram live transcription in a runtime integration.")
