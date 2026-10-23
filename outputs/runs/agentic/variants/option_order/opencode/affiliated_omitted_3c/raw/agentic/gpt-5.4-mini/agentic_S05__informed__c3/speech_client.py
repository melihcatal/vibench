import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str | None = None
    region: str | None = None
    language_code: str = "en-US"
    enable_punctuation: bool = True


def load_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        region=os.getenv("DEEPGRAM_REGION"),
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower()
        == "true",
    )


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())
