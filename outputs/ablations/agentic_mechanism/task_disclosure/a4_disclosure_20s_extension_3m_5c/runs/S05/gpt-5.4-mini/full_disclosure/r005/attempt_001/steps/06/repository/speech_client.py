import os
from dataclasses import dataclass
from typing import Optional

import openai


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"
    language: str = "en"
    temperature: float = 0.0


def get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def build_speech_client(api_key: Optional[str] = None) -> openai.AsyncOpenAI:
    return openai.AsyncOpenAI(api_key=get_api_key(api_key))


def resolve_speech_config(config: Optional[SpeechClientConfig] = None) -> SpeechClientConfig:
    if config is None:
        return SpeechClientConfig()
    return SpeechClientConfig(
        api_key=config.api_key,
        model=config.model or "gpt-4o-mini-transcribe",
        language=config.language or "en",
        temperature=config.temperature,
    )


def build_transcription_kwargs(config: Optional[SpeechClientConfig] = None) -> dict[str, object]:
    resolved = resolve_speech_config(config)
    return {
        "model": resolved.model,
        "language": resolved.language,
        "temperature": resolved.temperature,
    }
