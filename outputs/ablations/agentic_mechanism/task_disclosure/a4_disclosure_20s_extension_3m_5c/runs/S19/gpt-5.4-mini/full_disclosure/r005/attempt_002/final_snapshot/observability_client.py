import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


_DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass
class ObservabilityClientConfig:
    api_key: str
    app_key: str
    site: str = "datadoghq.com"
    timeout_seconds: int = 30

    @property
    def base_url(self) -> str:
        return f"https://api.{self.site}"


def _env(name: str, fallback: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    if value:
        return value
    return fallback


def load_config(
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: Optional[str] = None,
    timeout_seconds: Optional[int] = None,
) -> ObservabilityClientConfig:
    resolved_api_key = api_key or _env("DATADOG_API_KEY") or _env("DD_API_KEY")
    resolved_app_key = app_key or _env("DATADOG_APP_KEY") or _env("DD_APP_KEY")
    resolved_site = site or _env("DATADOG_SITE", "datadoghq.com") or "datadoghq.com"
    resolved_timeout = timeout_seconds or int(_env("OBSERVABILITY_TIMEOUT_SECONDS", "30") or "30")
    if not resolved_api_key or not resolved_app_key:
        raise EnvironmentError("DATADOG_API_KEY and DATADOG_APP_KEY are required")
    return ObservabilityClientConfig(
        api_key=resolved_api_key,
        app_key=resolved_app_key,
        site=resolved_site,
        timeout_seconds=resolved_timeout,
    )


class ManagedMetricsClient:
    def __init__(self, config: Optional[ObservabilityClientConfig] = None):
        self.config = config or load_config()

    @property
    def base_url(self) -> str:
        return self.config.base_url

    def headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "DD-API-KEY": self.config.api_key,
            "DD-APPLICATION-KEY": self.config.app_key,
        }

    def request(self, method: str, path: str, *, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.request(
            method=method,
            url=f"{self.base_url.rstrip('/')}/{path.lstrip('/')}",
            headers=self.headers(),
            params=params,
            json=json,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(float(value), tz=timezone.utc)
    elif isinstance(value, str):
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        raise TypeError(f"Unsupported timestamp type: {type(value)!r}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def resolve_time_window(from_ts: Any = None, to_ts: Any = None, *, default_minutes: int = 15) -> tuple[datetime, datetime]:
    to_dt = parse_datetime(to_ts) if to_ts is not None else datetime.now(timezone.utc)
    from_dt = parse_datetime(from_ts) if from_ts is not None else (to_dt - timedelta(minutes=default_minutes))
    return from_dt, to_dt


__all__ = ["ObservabilityClientConfig", "ManagedMetricsClient", "load_config", "parse_datetime", "resolve_time_window"]
