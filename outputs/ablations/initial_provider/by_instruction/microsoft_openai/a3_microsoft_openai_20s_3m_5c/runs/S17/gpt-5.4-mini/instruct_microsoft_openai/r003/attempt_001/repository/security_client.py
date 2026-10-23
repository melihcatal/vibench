import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class SecuritySettings:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "openai/gpt-5.4-mini"
    organization: Optional[str] = None


def load_settings() -> SecuritySettings:
    return SecuritySettings(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini"),
        organization=os.getenv("OPENAI_ORGANIZATION"),
    )


def build_client() -> OpenAI:
    settings = load_settings()
    return OpenAI(api_key=settings.api_key, base_url=settings.base_url, organization=settings.organization)


def model_name() -> str:
    return load_settings().model
