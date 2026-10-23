import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "alloy"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = DEFAULT_TTS_MODEL
    voice: str = DEFAULT_TTS_VOICE


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT"),
        model=os.getenv("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL),
        voice=os.getenv("OPENAI_TTS_VOICE", DEFAULT_TTS_VOICE),
    )


def create_speech_client(config: Optional[SpeechConfig] = None) -> OpenAI:
    cfg = config or load_speech_config()
    kwargs = {}
    if cfg.api_key is not None:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url is not None:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization is not None:
        kwargs["organization"] = cfg.organization
    if cfg.project is not None:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def resolve_tts_settings(
    model: Optional[str] = None,
    voice: Optional[str] = None,
    config: Optional[SpeechConfig] = None,
) -> tuple[str, str]:
    cfg = config or load_speech_config()
    return model or cfg.model, voice or cfg.voice
