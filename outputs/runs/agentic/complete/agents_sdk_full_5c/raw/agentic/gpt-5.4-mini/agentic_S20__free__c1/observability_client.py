from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from observability_models import LogEvent, LogQuery, normalize_query_response


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_key: str
    api_host: str = "https://api.datadoghq.com"


def load_datadog_config() -> DatadogConfig:
    api_key = os.getenv("DD_API_KEY", "")
    app_key = os.getenv("DD_APP_KEY", "")
    api_host = os.getenv("DD_SITE", "https://api.datadoghq.com")
    return DatadogConfig(api_key=api_key, app_key=app_key, api_host=api_host)


def _require_keys(config: DatadogConfig) -> None:
    if not config.api_key or not config.app_key:
        raise RuntimeError("DD_API_KEY and DD_APP_KEY are required for Datadog integrations")


def write_log_event(event: LogEvent, config: Optional[DatadogConfig] = None) -> Dict[str, Any]:
    config = config or load_datadog_config()
    _require_keys(config)
    payload = event.to_datadog_payload()
    return {
        "provider": "datadog",
        "api_host": config.api_host,
        "endpoint": f"{config.api_host}/api/v2/logs",
        "headers": {
            "DD-API-KEY": config.api_key,
            "DD-APPLICATION-KEY": config.app_key,
            "Content-Type": "application/json",
        },
        "payload": payload,
    }


def query_logs(query: LogQuery, config: Optional[DatadogConfig] = None) -> Dict[str, Any]:
    config = config or load_datadog_config()
    _require_keys(config)
    return {
        "provider": "datadog",
        "api_host": config.api_host,
        "endpoint": f"{config.api_host}/api/v2/logs/events/search",
        "headers": {
            "DD-API-KEY": config.api_key,
            "DD-APPLICATION-KEY": config.app_key,
            "Content-Type": "application/json",
        },
        "payload": query.to_datadog_payload(),
    }


def parse_logs_response(response: Any) -> Dict[str, Any]:
    return normalize_query_response(response)
