import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-5.4-mini"

    @classmethod
    def from_env(cls) -> "ModelClientConfig":
        return cls(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
            model=os.environ.get("OPENAI_MODEL", "gpt-5.4-mini"),
        )


def create_client(config: Optional[ModelClientConfig] = None) -> OpenAI:
    cfg = config or ModelClientConfig.from_env()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def generate_text(prompt: str, config: Optional[ModelClientConfig] = None) -> str:
    cfg = config or ModelClientConfig.from_env()
    client = create_client(cfg)
    response = client.responses.create(model=cfg.model, input=prompt)
    if getattr(response, "output_text", None):
        return response.output_text
    parts = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "".join(parts)


def get_model_metadata(config: Optional[ModelClientConfig] = None) -> Dict[str, Any]:
    cfg = config or ModelClientConfig.from_env()
    return {
        "provider": "openai",
        "model": cfg.model,
        "has_api_key": bool(cfg.api_key),
        "base_url": cfg.base_url,
    }
