import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class TranslationClientConfig:
    api_key: str
    base_url: Optional[str] = None
    model: str = "gpt-5.4-mini"
    organization: Optional[str] = None
    project: Optional[str] = None


def load_translation_client_config() -> TranslationClientConfig:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("TRANSLATION_API_KEY")
    if not api_key:
        raise ValueError("Missing API key: set OPENAI_API_KEY or TRANSLATION_API_KEY")
    return TranslationClientConfig(
        api_key=api_key,
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("TRANSLATION_MODEL", "gpt-5.4-mini"),
        organization=os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT"),
    )


def build_translation_client(config: Optional[TranslationClientConfig] = None) -> OpenAI:
    cfg = config or load_translation_client_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def resolve_translation_model(config: Optional[TranslationClientConfig] = None) -> str:
    return (config or load_translation_client_config()).model
