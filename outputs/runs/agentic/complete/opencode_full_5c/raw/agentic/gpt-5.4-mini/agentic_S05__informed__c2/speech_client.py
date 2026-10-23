import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SpeechConfig:
    api_key: str
    language: Optional[str] = None
    punctuate: bool = False


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("DEEPGRAM_API_KEY", ""),
        language=os.environ.get("STT_LANGUAGE"),
        punctuate=os.environ.get("STT_PUNCTUATE", "0") == "1",
    )


def deepgram_client():
    from deepgram import Deepgram

    return Deepgram(load_speech_config().api_key)
