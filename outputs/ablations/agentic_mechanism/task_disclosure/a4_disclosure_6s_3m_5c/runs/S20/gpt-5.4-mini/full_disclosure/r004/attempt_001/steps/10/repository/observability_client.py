import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class ObservabilityConfig:
    api_base_url: str
    api_key: str
    project_id: Optional[str] = None
    timeout_seconds: float = 30.0


def load_observability_config(env: Optional[Dict[str, str]] = None) -> ObservabilityConfig:
    source = env if env is not None else os.environ
    api_base_url = source.get("MANAGED_LOGGING_API_BASE_URL", "https://api.datadoghq.com")
    api_key = source.get("DATADOG_API_KEY", source.get("MANAGED_LOGGING_API_KEY", ""))
    project_id = source.get("MANAGED_LOGGING_PROJECT_ID")
    timeout_raw = source.get("MANAGED_LOGGING_TIMEOUT_SECONDS", "30")
    try:
        timeout_seconds = float(timeout_raw)
    except ValueError:
        timeout_seconds = 30.0
    return ObservabilityConfig(
        api_base_url=api_base_url.rstrip("/"),
        api_key=api_key,
        project_id=project_id,
        timeout_seconds=timeout_seconds,
    )


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or load_observability_config()
        self.session = session or requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        if self.config.project_id:
            headers["X-Project-Id"] = self.config.project_id
        return headers

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.session.get(
            f"{self.config.api_base_url}{path}",
            headers=self._headers(),
            params=params,
            timeout=self.config.timeout_seconds,
        )

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.session.post(
            f"{self.config.api_base_url}{path}",
            headers=self._headers(),
            json=json,
            timeout=self.config.timeout_seconds,
        )
