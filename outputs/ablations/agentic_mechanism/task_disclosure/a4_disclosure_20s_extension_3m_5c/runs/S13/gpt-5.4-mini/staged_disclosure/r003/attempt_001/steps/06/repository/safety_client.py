import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class SafetyConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "omni-moderation-latest"

    @classmethod
    def from_env(cls) -> "SafetyConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        )


def create_client(config: Optional[SafetyConfig] = None) -> OpenAI:
    cfg = config or SafetyConfig.from_env()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def moderate_text(text: str, config: Optional[SafetyConfig] = None) -> Dict[str, Any]:
    cfg = config or SafetyConfig.from_env()
    client = create_client(cfg)
    response = client.moderations.create(model=cfg.model, input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "model": cfg.model,
    }


def is_text_safe(text: str, config: Optional[SafetyConfig] = None) -> bool:
    return not moderate_text(text, config=config)["flagged"]
