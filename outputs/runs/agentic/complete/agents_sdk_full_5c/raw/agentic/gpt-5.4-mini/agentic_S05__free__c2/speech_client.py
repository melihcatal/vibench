from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import google.auth
from google.cloud import speech_v1p1beta1 as speech

DEFAULT_LANGUAGE_CODE = os.getenv("SPEECH_LANGUAGE_CODE", "en-US")
DEFAULT_MODEL = os.getenv("SPEECH_MODEL", "latest_long")
DEFAULT_ENABLE_PUNCTUATION = os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower() == "true"


@dataclass(frozen=True)
class SpeechConfig:
    language_code: str = DEFAULT_LANGUAGE_CODE
    model: str = DEFAULT_MODEL
    enable_automatic_punctuation: bool = DEFAULT_ENABLE_PUNCTUATION
    sample_rate_hz: int = int(os.getenv("SPEECH_SAMPLE_RATE_HZ", "16000"))
    encoding: str = os.getenv("SPEECH_ENCODING", "LINEAR16")


def get_speech_client() -> speech.SpeechClient:
    credentials, project = google.auth.default()
    return speech.SpeechClient(credentials=credentials)


def build_streaming_config(cfg: Optional[SpeechConfig] = None) -> speech.StreamingRecognitionConfig:
    cfg = cfg or SpeechConfig()
    recognition_config = speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, cfg.encoding),
        sample_rate_hertz=cfg.sample_rate_hz,
        language_code=cfg.language_code,
        model=cfg.model,
        enable_automatic_punctuation=cfg.enable_automatic_punctuation,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )


def stream_request(audio_content: bytes) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(audio_content=audio_content)
