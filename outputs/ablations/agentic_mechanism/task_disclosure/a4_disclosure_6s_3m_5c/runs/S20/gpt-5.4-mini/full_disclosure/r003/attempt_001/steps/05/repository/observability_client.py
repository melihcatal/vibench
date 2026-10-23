import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ObservabilityConfig:
    api_key: str
    project_id: Optional[str] = None
    base_url: str = "https://api.datadoghq.com/api/v2"
    logs_query_path: str = "/logs/events/search"
    logs_ingest_path: str = "/logs"


def load_config(env: Optional[Dict[str, str]] = None) -> ObservabilityConfig:
    source = env if env is not None else os.environ
    api_key = source.get("DATADOG_API_KEY", "").strip()
    if not api_key:
        raise ValueError("DATADOG_API_KEY is required")
    project_id = source.get("DATADOG_PROJECT_ID") or source.get("DD_PROJECT_ID")
    base_url = source.get("DATADOG_BASE_URL", "https://api.datadoghq.com/api/v2").rstrip("/")
    return ObservabilityConfig(api_key=api_key, project_id=project_id, base_url=base_url)


class ObservabilityClient:
    def __init__(self, config: ObservabilityConfig, session: Optional[requests.Session] = None) -> None:
        self.config = config
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        if self.config.project_id:
            self.session.headers.setdefault("DD-PROJECT-ID", self.config.project_id)

    def query_logs(self, payload: Dict[str, Any]) -> requests.Response:
        return self.session.post(f"{self.config.base_url}{self.config.logs_query_path}", json=payload, timeout=30)

    def ingest_log(self, payload: Dict[str, Any]) -> requests.Response:
        return self.session.post(f"{self.config.base_url}{self.config.logs_ingest_path}", json=payload, timeout=30)


def create_client(env: Optional[Dict[str, str]] = None, session: Optional[requests.Session] = None) -> ObservabilityClient:
    return ObservabilityClient(load_config(env), session=session)
