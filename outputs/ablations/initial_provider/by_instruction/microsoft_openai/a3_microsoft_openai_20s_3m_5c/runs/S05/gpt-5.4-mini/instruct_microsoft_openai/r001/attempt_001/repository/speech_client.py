import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class SpeechConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"
    language: str = "en"
    punctuation: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
        language=os.getenv("SPEECH_LANGUAGE", "en"),
        punctuation=os.getenv("SPEECH_PUNCTUATION", "true").lower() in {"1", "true", "yes", "on"},
    )


def create_openai_client(config: Optional[SpeechConfig] = None) -> OpenAI:
    cfg = config or load_speech_config()
    return OpenAI(api_key=cfg.api_key)


def speech_headers(config: Optional[SpeechConfig] = None) -> dict:
    cfg = config or load_speech_config()
    return {"OpenAI-Model": cfg.model, "OpenAI-Language": cfg.language}
