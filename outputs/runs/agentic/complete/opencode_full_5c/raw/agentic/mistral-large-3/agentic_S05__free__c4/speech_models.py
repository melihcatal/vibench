from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SpeechEvent:
    """Represents a speech recognition event."""

    transcript: str
    is_final: bool
    stability: float
    language_code: Optional[str] = None
    model: Optional[str] = None


@dataclass
class StreamingConfig:
    """Represents streaming recognition configuration."""

    language_code: str = "en-US"
    model: str = "latest_long"
    enable_punctuation: bool = True
    sample_rate_hertz: int = 16000


class SpeechNormalizer:
    """Provides normalization utilities for speech recognition responses."""

    @staticmethod
    def normalize_event(event: Dict[str, Any]) -> SpeechEvent:
        """Normalizes a raw speech event into a structured format."""
        return SpeechEvent(
            transcript=event.get("transcript", ""),
            is_final=event.get("is_final", False),
            stability=event.get("stability", 0.0),
            language_code=event.get("language_code"),
            model=event.get("model"),
        )

    @staticmethod
    def normalize_config(config: Dict[str, Any]) -> StreamingConfig:
        """Normalizes a raw config into a structured format."""
        return StreamingConfig(
            language_code=config.get("language_code", "en-US"),
            model=config.get("model", "latest_long"),
            enable_punctuation=config.get("enable_punctuation", True),
            sample_rate_hertz=config.get("sample_rate_hertz", 16000),
        )
