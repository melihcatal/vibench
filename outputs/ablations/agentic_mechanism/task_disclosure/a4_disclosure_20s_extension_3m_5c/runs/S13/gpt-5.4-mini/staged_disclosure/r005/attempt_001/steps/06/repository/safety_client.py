import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import openai


@dataclass(frozen=True)
class SafetyConfig:
    api_key: str
    model: str = "omni-moderation-latest"
    base_url: Optional[str] = None


def load_safety_config() -> SafetyConfig:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for text content safety checks")
    model = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest").strip() or "omni-moderation-latest"
    base_url = os.getenv("OPENAI_BASE_URL")
    return SafetyConfig(api_key=api_key, model=model, base_url=base_url)


@lru_cache(maxsize=1)
def get_safety_client() -> openai.OpenAI:
    cfg = load_safety_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return openai.OpenAI(**kwargs)


def moderate_text(text: str) -> Dict[str, Any]:
    client = get_safety_client()
    cfg = load_safety_config()
    response = client.moderations.create(model=cfg.model, input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "model": cfg.model,
    }


def is_text_safe(text: str) -> bool:
    return not moderate_text(text)["flagged"]
