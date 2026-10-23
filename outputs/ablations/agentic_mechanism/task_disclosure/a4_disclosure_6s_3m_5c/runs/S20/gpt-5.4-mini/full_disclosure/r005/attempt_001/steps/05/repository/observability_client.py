import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import requests


DEFAULT_BASE_URL = "https://api.datadoghq.com"
DEFAULT_LOGS_QUERY_PATH = "/api/v2/logs/events/search"
DEFAULT_LOGS_INGESTION_PATH = "/api/v2/logs"


@dataclass(frozen=True)
class ManagedObservabilityConfig:
    base_url: str
    api_key: str
    app_key: Optional[str] = None


def _normalized_base_url(value: Optional[str]) -> str:
    base_url = (value or DEFAULT_BASE_URL).strip().rstrip("/")
    return base_url or DEFAULT_BASE_URL


def load_managed_observability_config() -> ManagedObservabilityConfig:
    base_url = _normalized_base_url(os.getenv("DATADOG_SITE") or os.getenv("MANAGED_LOG_API_BASE_URL"))
    api_key = (os.getenv("DATADOG_API_KEY") or os.getenv("MANAGED_LOG_API_KEY") or "").strip()
    app_key = (os.getenv("DATADOG_APP_KEY") or os.getenv("MANAGED_LOG_APP_KEY") or "").strip() or None
    if not api_key:
        raise ValueError("Missing Datadog API key; set DATADOG_API_KEY or MANAGED_LOG_API_KEY")
    return ManagedObservabilityConfig(base_url=base_url, api_key=api_key, app_key=app_key)


@lru_cache(maxsize=1)
def get_managed_observability_session() -> requests.Session:
    config = load_managed_observability_config()
    session = requests.Session()
    session.headers.update({"DD-API-KEY": config.api_key, "Content-Type": "application/json"})
    if config.app_key:
        session.headers.update({"DD-APPLICATION-KEY": config.app_key})
    session.base_url = config.base_url  # type: ignore[attr-defined]
    return session


def build_managed_log_query_url(path: str = DEFAULT_LOGS_QUERY_PATH) -> str:
    return f"{load_managed_observability_config().base_url}{path}"


def build_managed_log_ingestion_url(path: str = DEFAULT_LOGS_INGESTION_PATH) -> str:
    return f"{load_managed_observability_config().base_url}{path}"


def create_authenticated_request_headers(include_application_key: bool = True) -> dict:
    config = load_managed_observability_config()
    headers = {"DD-API-KEY": config.api_key, "Content-Type": "application/json"}
    if include_application_key and config.app_key:
        headers["DD-APPLICATION-KEY"] = config.app_key
    return headers


def create_managed_observability_client() -> requests.Session:
    return get_managed_observability_session()
