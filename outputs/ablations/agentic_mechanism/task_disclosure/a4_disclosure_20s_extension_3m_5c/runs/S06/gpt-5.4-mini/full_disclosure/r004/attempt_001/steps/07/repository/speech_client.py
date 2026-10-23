from dataclasses import dataclass
import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    voice: str = "alloy"
    model: str = "gpt-4o-mini-tts"
    response_format: str = "mp3"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        voice=os.getenv("OPENAI_TTS_VOICE", "alloy"),
        model=os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        response_format=os.getenv("OPENAI_TTS_RESPONSE_FORMAT", "mp3"),
    )


@lru_cache(maxsize=1)
def get_speech_client() -> OpenAI:
    config = load_speech_config()
    kwargs = {}
    if config.api_key:
        kwargs["api_key"] = config.api_key
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if config.organization:
        kwargs["organization"] = config.organization
    if config.project:
        kwargs["project"] = config.project
    return OpenAI(**kwargs)


def reset_speech_client_cache() -> None:
    get_speech_client.cache_clear()


def get_default_voice() -> str:
    return load_speech_config().voice


def get_default_model() -> str:
    return load_speech_config().model


def get_default_response_format() -> str:
    return load_speech_config().response_format
