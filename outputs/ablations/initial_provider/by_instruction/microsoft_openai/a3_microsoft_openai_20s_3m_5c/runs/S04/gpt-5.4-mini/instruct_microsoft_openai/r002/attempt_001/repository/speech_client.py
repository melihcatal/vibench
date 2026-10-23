import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class SpeechConfig:
    api_key: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"


def load_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        model=os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
    )


def get_client(config: Optional[SpeechConfig] = None) -> OpenAI:
    cfg = config or load_config()
    return OpenAI(api_key=cfg.api_key, organization=cfg.organization, project=cfg.project)


def get_model(config: Optional[SpeechConfig] = None) -> str:
    return (config or load_config()).model
