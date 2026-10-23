import os
from dataclasses import dataclass

from anthropic import Anthropic


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class ModelSettings:
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 1024
    temperature: float = 0.2


def load_settings() -> ModelSettings:
    return ModelSettings(
        model=_env("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=int(_env("ANTHROPIC_MAX_TOKENS", "1024")),
        temperature=float(_env("ANTHROPIC_TEMPERATURE", "0.2")),
    )


def create_client() -> Anthropic:
    return Anthropic(api_key=_env("ANTHROPIC_API_KEY"))


def build_messages(system: str, user: str):
    return [{"role": "user", "content": user}], system
