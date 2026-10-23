import os
from dataclasses import dataclass
from typing import Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"

    @classmethod
    def from_env(cls) -> "SpeechConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID"),
            model=os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
        )


def build_client(config: Optional[SpeechConfig] = None) -> OpenAI:
    cfg = config or SpeechConfig.from_env()
    kwargs: Dict[str, str] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def streaming_stt_config(config: Optional[SpeechConfig] = None) -> Dict[str, str]:
    cfg = config or SpeechConfig.from_env()
    return {
        "provider": "openai",
        "model": cfg.model,
        "api_key_env": "OPENAI_API_KEY",
        "base_url_env": "OPENAI_BASE_URL",
        "organization_env": "OPENAI_ORG_ID",
        "project_env": "OPENAI_PROJECT_ID",
        "transcription_endpoint": "/v1/audio/transcriptions",
    }
