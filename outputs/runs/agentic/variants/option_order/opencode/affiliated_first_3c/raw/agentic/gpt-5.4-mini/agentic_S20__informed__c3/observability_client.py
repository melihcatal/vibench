import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


@dataclass
class ObservabilityConfig:
    base_url: str
    api_key: str
    app_key: Optional[str] = None
    ingestion_path: str = "/api/v2/logs"
    query_path: str = "/api/v2/logs/events/search"


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        base_url=os.getenv("DATADOG_API_BASE_URL", "https://api.datadoghq.com"),
        api_key=os.environ["DD_API_KEY"],
        app_key=os.getenv("DD_APP_KEY"),
    )


def _headers(cfg: ObservabilityConfig) -> Dict[str, str]:
    headers = {"DD-API-KEY": cfg.api_key, "Content-Type": "application/json"}
    if cfg.app_key:
        headers["DD-APPLICATION-KEY"] = cfg.app_key
    return headers


class DatadogLogsClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None) -> None:
        self.config = config or load_config()

    def ingest(self, logs: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        payload = list(logs)
        response = requests.post(
            f"{self.config.base_url}{self.config.ingestion_path}",
            headers=_headers(self.config),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return {"status_code": response.status_code, "body": response.json() if response.content else None}

    def query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.config.base_url}{self.config.query_path}",
            headers=_headers(self.config),
            json=query,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
