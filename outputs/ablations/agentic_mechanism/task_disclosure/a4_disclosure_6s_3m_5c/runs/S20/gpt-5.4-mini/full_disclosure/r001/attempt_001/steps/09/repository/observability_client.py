import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class ObservabilityConfig:
    api_key: str
    base_url: str
    query_model: str
    ingest_model: str
    organization: Optional[str] = None
    project: Optional[str] = None


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_config() -> ObservabilityConfig:
    api_key = _env("OPENAI_API_KEY") or ""
    base_url = _env("OPENAI_BASE_URL", "https://api.openai.com/v1")
    query_model = _env("OBSERVABILITY_QUERY_MODEL", "gpt-5.4-mini")
    ingest_model = _env("OBSERVABILITY_INGEST_MODEL", "gpt-5.4-mini")
    organization = _env("OPENAI_ORG_ID")
    project = _env("OPENAI_PROJECT")
    return ObservabilityConfig(
        api_key=api_key,
        base_url=base_url,
        query_model=query_model,
        ingest_model=ingest_model,
        organization=organization,
        project=project,
    )


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    config = load_config()
    kwargs: Dict[str, Any] = {"api_key": config.api_key, "base_url": config.base_url}
    if config.organization:
        kwargs["organization"] = config.organization
    if config.project:
        kwargs["project"] = config.project
    return OpenAI(**kwargs)


def get_query_model() -> str:
    return load_config().query_model


def get_ingest_model() -> str:
    return load_config().ingest_model


def get_default_headers() -> Dict[str, str]:
    return {"X-Observability-Client": "managed-log-query"}


def reset_client_cache() -> None:
    get_client.cache_clear()
