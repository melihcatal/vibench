import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import speech_v1


@dataclass(frozen=True)
class SpeechConfig:
    language_code: str = os.getenv("SPEECH_LANGUAGE_CODE", "en-US")
    sample_rate_hertz: int = int(os.getenv("SPEECH_SAMPLE_RATE_HERTZ", "16000"))
    encoding: str = os.getenv("SPEECH_ENCODING", "LINEAR16")
    model: str = os.getenv("SPEECH_MODEL", "latest_long")
    interim_results: bool = os.getenv("SPEECH_INTERIM_RESULTS", "true").lower() in {"1", "true", "yes", "on"}
    enable_automatic_punctuation: bool = os.getenv("SPEECH_ENABLE_AUTOMATIC_PUNCTUATION", "true").lower() in {"1", "true", "yes", "on"}
    single_utterance: bool = os.getenv("SPEECH_SINGLE_UTTERANCE", "false").lower() in {"1", "true", "yes", "on"}


def load_speech_config(overrides: Optional[Dict[str, Any]] = None) -> SpeechConfig:
    base = SpeechConfig()
    if not overrides:
        return base
    data = {
        "language_code": overrides.get("language_code", base.language_code),
        "sample_rate_hertz": int(overrides.get("sample_rate_hertz", base.sample_rate_hertz)),
        "encoding": overrides.get("encoding", base.encoding),
        "model": overrides.get("model", base.model),
        "interim_results": bool(overrides.get("interim_results", base.interim_results)),
        "enable_automatic_punctuation": bool(overrides.get("enable_automatic_punctuation", base.enable_automatic_punctuation)),
        "single_utterance": bool(overrides.get("single_utterance", base.single_utterance)),
    }
    return SpeechConfig(**data)


def create_streaming_client() -> speech_v1.SpeechClient:
    return speech_v1.SpeechClient()


def build_streaming_recognition_config(config: Optional[SpeechConfig] = None) -> speech_v1.StreamingRecognitionConfig:
    cfg = config or SpeechConfig()
    recognition_config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding[cfg.encoding],
        sample_rate_hertz=cfg.sample_rate_hertz,
        language_code=cfg.language_code,
        model=cfg.model,
        enable_automatic_punctuation=cfg.enable_automatic_punctuation,
    )
    return speech_v1.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=cfg.interim_results,
        single_utterance=cfg.single_utterance,
    )


def build_streaming_request(audio_content: bytes) -> speech_v1.StreamingRecognizeRequest:
    return speech_v1.StreamingRecognizeRequest(audio_content=audio_content)


def make_streaming_requests(audio_chunks):
    for chunk in audio_chunks:
        yield build_streaming_request(chunk)
