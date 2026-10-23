import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class ObservabilityConfig:
    datadog_api_key: str
    datadog_app_key: str
    datadog_site: str = "datadoghq.com"
    timeout_seconds: int = 30

    @property
    def base_url(self) -> str:
        return f"https://api.{self.datadog_site}"


def _env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        datadog_api_key=_env("DATADOG_API_KEY"),
        datadog_app_key=_env("DATADOG_APP_KEY"),
        datadog_site=os.getenv("DATADOG_SITE", "datadoghq.com"),
        timeout_seconds=int(os.getenv("DATADOG_TIMEOUT_SECONDS", "30")),
    )


def build_session(config: Optional[ObservabilityConfig] = None) -> requests.Session:
    cfg = config or load_config()
    session = requests.Session()
    session.headers.update(
        {
            "DD-API-KEY": cfg.datadog_api_key,
            "DD-APPLICATION-KEY": cfg.datadog_app_key,
            "Accept": "application/json",
        }
    )
    session.timeout = cfg.timeout_seconds
    return session


def build_metrics_url(config: Optional[ObservabilityConfig] = None, path: str = "/api/v1/query") -> str:
    cfg = config or load_config()
    return f"{cfg.base_url}{path}"


__all__ = ["ObservabilityConfig", "load_config", "build_session", "build_metrics_url"]
