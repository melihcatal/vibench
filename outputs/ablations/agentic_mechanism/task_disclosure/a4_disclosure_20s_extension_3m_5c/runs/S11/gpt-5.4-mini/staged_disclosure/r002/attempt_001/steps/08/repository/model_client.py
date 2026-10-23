import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import openai


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


@dataclass(frozen=True)
class ManagedModelConfig:
    api_key: str
    base_url: str
    model: str = DEFAULT_MODEL

    @classmethod
    def from_env(cls) -> "ManagedModelConfig":
        api_key = _env("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        base_url = _env("OPENAI_BASE_URL", "https://api.openai.com/v1")
        model = _env("OPENAI_MODEL", DEFAULT_MODEL) or DEFAULT_MODEL
        return cls(api_key=api_key, base_url=base_url, model=model)


class ManagedModelClient:
    def __init__(self, config: Optional[ManagedModelConfig] = None) -> None:
        self.config = config or ManagedModelConfig.from_env()
        self._client = openai.OpenAI(api_key=self.config.api_key, base_url=self.config.base_url)

    def chat(self, messages: Any, **kwargs: Any) -> str:
        response = self._client.chat.completions.create(model=self.config.model, messages=messages, **kwargs)
        return response.choices[0].message.content or ""

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    def raw_client(self) -> openai.OpenAI:
        return self._client


def load_config() -> Dict[str, str]:
    config = ManagedModelConfig.from_env()
    return {"api_key": config.api_key, "base_url": config.base_url, "model": config.model}


def get_client(config: Optional[ManagedModelConfig] = None) -> ManagedModelClient:
    return ManagedModelClient(config=config)
