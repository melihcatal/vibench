from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, Optional

from google.cloud import speech

from speech_models import AudioChunk, StreamingRecognitionConfig, TranscriptSegment


@dataclass
class SpeechClientConfig:
    language_code: str = os.getenv("SPEECH_LANGUAGE_CODE", "en-US")
    enable_automatic_punctuation: bool = os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower() == "true"
    model: str = os.getenv("GOOGLE_SPEECH_MODEL", "chirp")
    sample_rate_hz: int = int(os.getenv("SPEECH_SAMPLE_RATE_HZ", "16000"))


class SpeechClientHelper:
    def __init__(self, config: Optional[SpeechClientConfig] = None) -> None:
        self.config = config or SpeechClientConfig()
        self._client = speech.SpeechClient()

    def build_streaming_config(self, language_code: Optional[str] = None) -> speech.StreamingRecognitionConfig:
        cfg = StreamingRecognitionConfig(
            language_code=language_code or self.config.language_code,
            enable_automatic_punctuation=self.config.enable_automatic_punctuation,
            model=self.config.model,
        )
        return speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.config.sample_rate_hz,
                language_code=cfg.language_code,
                enable_automatic_punctuation=cfg.enable_automatic_punctuation,
                model=cfg.model,
            ),
            interim_results=cfg.interim_results,
            single_utterance=cfg.single_utterance,
        )

    def response_to_segments(self, response: speech.StreamingRecognizeResponse) -> Iterable[TranscriptSegment]:
        for result in response.results:
            if not result.alternatives:
                continue
            alternative = result.alternatives[0]
            yield TranscriptSegment(
                text=alternative.transcript,
                is_final=result.is_final,
                language=self.config.language_code,
                confidence=getattr(alternative, "confidence", None),
                raw={"result_end_time": str(getattr(result, "result_end_time", ""))},
            )

    def stream_audio(self, chunks: Iterable[AudioChunk], language_code: Optional[str] = None):
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk.data) for chunk in chunks
        )
        return self._client.streaming_recognize(self.build_streaming_config(language_code), requests)
