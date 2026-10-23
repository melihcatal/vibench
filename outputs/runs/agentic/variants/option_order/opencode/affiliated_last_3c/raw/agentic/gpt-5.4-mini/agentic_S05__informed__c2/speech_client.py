import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    api_key: str
    language: str = "en-US"
    punctuate: bool = True
    interim_results: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("DEEPGRAM_API_KEY", ""),
        language=os.getenv("SPEECH_LANGUAGE", "en-US"),
        punctuate=os.getenv("SPEECH_PUNCTUATE", "true").lower() == "true",
        interim_results=os.getenv("SPEECH_INTERIM_RESULTS", "true").lower() == "true",
    )


def build_deepgram_client():
    from deepgram import Deepgram

    config = load_speech_config()
    return Deepgram(config.api_key)


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())
