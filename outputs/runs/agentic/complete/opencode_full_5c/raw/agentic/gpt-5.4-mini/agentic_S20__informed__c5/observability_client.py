import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_key: str
    site: str
    service: str
    source: str
    host: str


def load_datadog_config() -> DatadogConfig:
    return DatadogConfig(
        api_key=os.environ["DD_API_KEY"],
        app_key=os.environ["DD_APP_KEY"],
        site=os.getenv("DD_SITE", "datadoghq.com"),
        service=os.getenv("DD_SERVICE", "log-query-service"),
        source=os.getenv("DD_SOURCE", "python"),
        host=os.getenv("DD_HOST", "localhost"),
    )


def datadog_headers(config: DatadogConfig) -> Dict[str, str]:
    return {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }


def datadog_api_base(config: DatadogConfig) -> str:
    return f"https://api.{config.site}"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def post_json(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    if response.content:
        return response.json()
    return {}


def get_json(url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None, timeout: int = 30) -> Dict[str, Any]:
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()
