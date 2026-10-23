import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import openai


@dataclass
class SpeechClientConfig:
    api_key: str
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL"),
        organization=os.environ.get("OPENAI_ORG_ID"),
        project=os.environ.get("OPENAI_PROJECT_ID"),
    )


def build_client() -> openai.OpenAI:
    cfg = load_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return openai.OpenAI(**kwargs)


def get_openai_audio_model() -> str:
    return os.environ.get("OPENAI_AUDIO_MODEL", "gpt-4o-mini-transcribe")


def get_openai_text_model() -> str:
    return os.environ.get("OPENAI_TEXT_MODEL", "gpt-4o-mini")
