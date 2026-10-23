import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SpeechConfig:
    api_key: str = field(
        default_factory=lambda: os.environ.get("ASSEMBLYAI_API_KEY", "")
    )
    api_base_url: str = "https://api.assemblyai.com/v2"
    polling_interval_seconds: int = 5
    max_poll_attempts: int = 120
    default_language_code: str = "en"
    default_audio_format: str = "mp3"
    default_sample_rate: int = 16000


def get_assemblyai_headers(config: Optional[SpeechConfig] = None) -> dict:
    cfg = config or SpeechConfig()
    return {
        "authorization": cfg.api_key,
        "content-type": "application/json",
    }


def build_transcription_payload(
    audio_url: str,
    config: Optional[SpeechConfig] = None,
    **kwargs,
) -> dict:
    cfg = config or SpeechConfig()
    payload = {
        "audio_url": audio_url,
        "language_code": kwargs.get("language_code", cfg.default_language_code),
    }
    if kwargs.get("speaker_labels"):
        payload["speaker_labels"] = True
    if kwargs.get("word_boost"):
        payload["word_boost"] = kwargs["word_boost"]
    if kwargs.get("boost_param"):
        payload["boost_param"] = kwargs["boost_param"]
    if kwargs.get("punctuate") is not None:
        payload["punctuate"] = kwargs["punctuate"]
    if kwargs.get("format_text") is not None:
        payload["format_text"] = kwargs["format_text"]
    if kwargs.get("disfluencies") is not None:
        payload["disfluencies"] = kwargs["disfluencies"]
    return payload


def build_diarization_payload(
    audio_url: str,
    config: Optional[SpeechConfig] = None,
    **kwargs,
) -> dict:
    cfg = config or SpeechConfig()
    payload = {
        "audio_url": audio_url,
        "language_code": kwargs.get("language_code", cfg.default_language_code),
        "speaker_labels": True,
    }
    if kwargs.get("punctuate") is not None:
        payload["punctuate"] = kwargs["punctuate"]
    if kwargs.get("format_text") is not None:
        payload["format_text"] = kwargs["format_text"]
    return payload


def build_timestamp_payload(
    audio_url: str,
    config: Optional[SpeechConfig] = None,
    **kwargs,
) -> dict:
    cfg = config or SpeechConfig()
    payload = {
        "audio_url": audio_url,
        "language_code": kwargs.get("language_code", cfg.default_language_code),
        "word_boost": kwargs.get("word_boost", []),
    }
    if kwargs.get("punctuate") is not None:
        payload["punctuate"] = kwargs["punctuate"]
    return payload
