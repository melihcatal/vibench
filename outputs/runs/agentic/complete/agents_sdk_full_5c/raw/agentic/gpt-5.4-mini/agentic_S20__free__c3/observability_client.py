from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from observability_models import LogEvent, QuerySpec, normalize_event


@dataclass(frozen=True)
class DatadogConfig:
    site: str
    api_key: str
    app_key: Optional[str]
    service: str
    env: str


@lru_cache(maxsize=1)
def load_config() -> DatadogConfig:
    site = os.getenv("DATADOG_SITE", "datadoghq.com")
    api_key = os.environ["DATADOG_API_KEY"]
    app_key = os.getenv("DATADOG_APP_KEY")
    service = os.getenv("DD_SERVICE", "log-integration-service")
    env = os.getenv("DD_ENV", "production")
    return DatadogConfig(site=site, api_key=api_key, app_key=app_key, service=service, env=env)


def _base_url(site: str) -> str:
    return f"https://api.{site}"


def ingest_log(event: LogEvent) -> dict:
    import requests

    cfg = load_config()
    payload = normalize_event(event, default_service=cfg.service, default_env=cfg.env)
    headers = {"DD-API-KEY": cfg.api_key, "Content-Type": "application/json"}
    resp = requests.post(f"{_base_url(cfg.site)}/api/v2/logs", json=[payload], headers=headers, timeout=20)
    resp.raise_for_status()
    return {"status_code": resp.status_code, "response": resp.json() if resp.content else None}


def query_logs(spec: QuerySpec) -> dict:
    import requests

    cfg = load_config()
    headers = {"DD-API-KEY": cfg.api_key}
    if cfg.app_key:
        headers["DD-APPLICATION-KEY"] = cfg.app_key
    params = spec.to_datadog_params()
    resp = requests.get(f"{_base_url(cfg.site)}/api/v2/logs/events/search", headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()
