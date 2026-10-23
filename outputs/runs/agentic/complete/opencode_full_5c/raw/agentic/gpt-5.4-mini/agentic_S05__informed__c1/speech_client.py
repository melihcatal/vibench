import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str | None = None
    url: str | None = None
    language: str = "en-US"
    enable_punctuation: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("IBM_STT_APIKEY")
        or os.getenv("DEEPGRAM_API_KEY")
        or os.getenv("AZURE_SPEECH_KEY"),
        url=os.getenv("IBM_STT_URL")
        or os.getenv("DEEPGRAM_URL")
        or os.getenv("AZURE_SPEECH_REGION"),
        language=os.getenv("SPEECH_LANGUAGE", "en-US"),
        enable_punctuation=os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower()
        == "true",
    )


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())
