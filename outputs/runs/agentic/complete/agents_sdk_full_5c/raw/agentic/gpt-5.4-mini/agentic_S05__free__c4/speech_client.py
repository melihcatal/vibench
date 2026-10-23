from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, AsyncIterable, AsyncIterator, Dict, Iterable, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_models import CaptionChunk, SpeechStreamConfig, normalize_transcript_text


@dataclass(frozen=True)
class SpeechClientConfig:
    project_id: Optional[str] = None
    language_code: str = "en-US"
    location: Optional[str] = None


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    )


def build_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def build_streaming_config(settings: SpeechStreamConfig) -> speech.StreamingRecognitionConfig:
    encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
    if settings.encoding.upper() == "FLAC":
        encoding = speech.RecognitionConfig.AudioEncoding.FLAC
    recognition_config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=settings.sample_rate_hz,
        language_code=settings.language_code,
        enable_automatic_punctuation=settings.punctuation,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=settings.interim_results,
        single_utterance=False,
    )


async def chunk_audio_stream(source: AsyncIterable[bytes]) -> AsyncIterator[speech.StreamingRecognizeRequest]:
    async for audio in source:
        yield speech.StreamingRecognizeRequest(audio_content=audio)


def microphone_requests(audio_chunks: Iterable[bytes]) -> Iterable[speech.StreamingRecognizeRequest]:
    for audio in audio_chunks:
        yield speech.StreamingRecognizeRequest(audio_content=audio)


def extract_transcript(response: Any) -> Optional[CaptionChunk]:
    results = getattr(response, "results", None) or []
    if not results:
        return None
    result = results[0]
    alternatives = getattr(result, "alternatives", None) or []
    if not alternatives:
        return None
    alt = alternatives[0]
    text = normalize_transcript_text(getattr(alt, "transcript", ""))
    return CaptionChunk(
        text=text,
        start_ms=None,
        end_ms=None,
    )
