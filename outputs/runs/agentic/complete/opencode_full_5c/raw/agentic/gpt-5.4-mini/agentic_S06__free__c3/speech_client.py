import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class SpeechConfig:
    api_key: str
    organization: str | None = None
    project: str | None = None
    default_voice: str = "alloy"
    default_format: str = "mp3"
    model: str = "gpt-4o-mini-tts"


def load_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        organization=os.environ.get("OPENAI_ORG_ID"),
        project=os.environ.get("OPENAI_PROJECT_ID"),
        default_voice=os.environ.get("OPENAI_TTS_VOICE", "alloy"),
        default_format=os.environ.get("OPENAI_TTS_FORMAT", "mp3"),
        model=os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
    )


def build_client(config: SpeechConfig | None = None) -> OpenAI:
    cfg = config or load_config()
    return OpenAI(
        api_key=cfg.api_key, organization=cfg.organization, project=cfg.project
    )


def resolve_voice(voice: str | None = None) -> str:
    return voice or load_config().default_voice


def resolve_format(audio_format: str | None = None) -> str:
    return audio_format or load_config().default_format
