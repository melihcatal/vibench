import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SpeechClientConfig:
    project_id: str = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT", "")
    )
    location: str = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )
    credentials_path: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    api_endpoint: str = "speech.googleapis.com"
    model: str = "latest_long"
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    max_alternatives: int = 1
    profanity_filter: bool = False
    sample_rate_hertz: int = 16000
    audio_encoding: str = "LINEAR16"


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig()


def build_recognizer_path(config: SpeechClientConfig) -> str:
    return f"projects/{config.project_id}/locations/{config.location}/recognizers/_"


def build_streaming_config(config: SpeechClientConfig) -> dict:
    return {
        "features": {
            "enable_automatic_punctuation": config.enable_automatic_punctuation,
            "enable_word_time_offsets": config.enable_word_time_offsets,
            "profanity_filter": config.profanity_filter,
            "model": config.model,
        },
        "config": {
            "auto_decoding_config": {},
            "language_codes": [config.language_code],
            "max_alternatives": config.max_alternatives,
        },
    }


def validate_config(config: SpeechClientConfig) -> None:
    if not config.project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    if config.credentials_path and not os.path.exists(config.credentials_path):
        raise FileNotFoundError(
            f"Credentials file not found: {config.credentials_path}"
        )
