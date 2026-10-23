from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_key: str
    site: str = "datadoghq.com"

    @property
    def api_base_url(self) -> str:
        return f"https://api.{self.site}"


def load_datadog_config() -> DatadogConfig:
    api_key = os.getenv("DD_API_KEY", "")
    app_key = os.getenv("DD_APP_KEY", "")
    site = os.getenv("DD_SITE", "datadoghq.com")
    return DatadogConfig(api_key=api_key, app_key=app_key, site=site)


def create_session(config: Optional[DatadogConfig] = None) -> requests.Session:
    cfg = config or load_datadog_config()
    session = requests.Session()
    session.headers.update(
        {
            "DD-API-KEY": cfg.api_key,
            "DD-APPLICATION-KEY": cfg.app_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    return session


def datadog_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
    config: Optional[DatadogConfig] = None,
) -> Dict[str, Any]:
    cfg = config or load_datadog_config()
    session = create_session(cfg)
    response = session.get(f"{cfg.api_base_url}{path}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()
