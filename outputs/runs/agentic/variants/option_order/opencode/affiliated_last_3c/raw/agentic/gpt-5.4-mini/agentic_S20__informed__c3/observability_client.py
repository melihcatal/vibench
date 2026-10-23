import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class ObservabilityConfig:
    api_key: str
    app_key: Optional[str]
    site: str
    service: str
    source: str
    host: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        api_key=os.environ.get("DD_API_KEY", ""),
        app_key=os.environ.get("DD_APP_KEY"),
        site=os.environ.get("DD_SITE", "datadoghq.com"),
        service=os.environ.get("OBSERVABILITY_SERVICE", "checkout-api"),
        source=os.environ.get("OBSERVABILITY_SOURCE", "python"),
        host=os.environ.get("OBSERVABILITY_HOST", os.uname().nodename),
    )


def datadog_logs_base_url(site: str) -> str:
    return f"https://http-intake.logs.{site}/api/v2"


def datadog_query_url(site: str) -> str:
    return f"https://api.{site}/api/v2/logs/events/search"


def datadog_headers(config: ObservabilityConfig) -> Dict[str, str]:
    headers = {"Content-Type": "application/json", "DD-API-KEY": config.api_key}
    if config.app_key:
        headers["DD-APPLICATION-KEY"] = config.app_key
    return headers


def post_json(
    url: str, headers: Dict[str, str], payload: Dict[str, Any]
) -> Dict[str, Any]:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json() if response.text else {}


def get_json(
    url: str, headers: Dict[str, str], params: Dict[str, Any]
) -> Dict[str, Any]:
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json() if response.text else {}
