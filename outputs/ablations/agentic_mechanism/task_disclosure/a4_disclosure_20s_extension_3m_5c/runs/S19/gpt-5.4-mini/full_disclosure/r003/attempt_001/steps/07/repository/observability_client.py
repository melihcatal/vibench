from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import requests


DEFAULT_BASE_URL = "https://api.datadoghq.com"
DEFAULT_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class ObservabilityConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    app_key: Optional[str] = None
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS


def load_config() -> ObservabilityConfig:
    api_key = os.getenv("DATADOG_API_KEY") or os.getenv("DD_API_KEY") or ""
    if not api_key:
        raise ValueError("Missing DATADOG_API_KEY")
    base_url = os.getenv("DATADOG_BASE_URL") or os.getenv("DD_SITE_URL") or DEFAULT_BASE_URL
    app_key = os.getenv("DATADOG_APP_KEY") or os.getenv("DD_APP_KEY")
    timeout_raw = os.getenv("OBSERVABILITY_TIMEOUT_SECONDS")
    timeout_seconds = float(timeout_raw) if timeout_raw else DEFAULT_TIMEOUT_SECONDS
    return ObservabilityConfig(api_key=api_key, base_url=base_url.rstrip("/"), app_key=app_key, timeout_seconds=timeout_seconds)


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None) -> None:
        self.config = config or load_config()
        self._session = requests.Session()
        self._session.headers.update({
            "DD-API-KEY": self.config.api_key,
            "Accept": "application/json",
        })
        if self.config.app_key:
            self._session.headers["DD-APPLICATION-KEY"] = self.config.app_key

    @property
    def base_url(self) -> str:
        return self.config.base_url

    @property
    def timeout_seconds(self) -> float:
        return self.config.timeout_seconds

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method: str, path: str, **kwargs):
        kwargs.setdefault("timeout", self.timeout_seconds)
        return self._session.request(method=method, url=self.url(path), **kwargs)


@lru_cache(maxsize=1)
def get_observability_client() -> ObservabilityClient:
    return ObservabilityClient()
