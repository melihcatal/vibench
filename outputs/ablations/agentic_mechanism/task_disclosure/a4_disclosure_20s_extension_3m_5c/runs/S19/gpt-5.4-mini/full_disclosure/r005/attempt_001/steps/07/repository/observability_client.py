import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import requests


DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class ObservabilityConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def load_config(api_key: Optional[str] = None, base_url: Optional[str] = None, timeout_seconds: Optional[float] = None) -> ObservabilityConfig:
    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY") or ""
    resolved_base_url = (base_url or os.getenv("OPENAI_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    resolved_timeout = timeout_seconds if timeout_seconds is not None else _env_float("OPENAI_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)
    return ObservabilityConfig(api_key=resolved_api_key, base_url=resolved_base_url, timeout_seconds=resolved_timeout)


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None):
        self.config = config or load_config()

    @property
    def headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    @lru_cache(maxsize=1)
    def session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(self.headers)
        return session

    def request(self, method: str, path: str, **kwargs):
        url = f"{self.config.base_url}/{path.lstrip('/')}"
        timeout = kwargs.pop("timeout", self.config.timeout_seconds)
        return self.session().request(method=method, url=url, timeout=timeout, **kwargs)


def get_client(api_key: Optional[str] = None, base_url: Optional[str] = None, timeout_seconds: Optional[float] = None) -> ObservabilityClient:
    return ObservabilityClient(load_config(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds))
