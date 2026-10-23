from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class SpeechConfig:
    api_key: Optional[str]
    url: Optional[str]
    language_code: str
    punctuation: bool


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        url=os.getenv("DEEPGRAM_URL", "wss://api.deepgram.com/v1/listen"),
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        punctuation=os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower()
        in {"1", "true", "yes", "on"},
    )
