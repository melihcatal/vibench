import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class ObservabilityConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    default_hours: int = 24


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        default_hours=int(os.getenv("OBSERVABILITY_DEFAULT_HOURS", "24")),
    )


def get_client() -> OpenAI:
    cfg = load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def time_range(hours: Optional[int] = None) -> Dict[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours if hours is not None else load_config().default_hours)
    return {"start": start.isoformat(), "end": end.isoformat()}


def with_time_range(payload: Dict[str, Any], hours: Optional[int] = None) -> Dict[str, Any]:
    merged = dict(payload)
    merged.update(time_range(hours))
    return merged
