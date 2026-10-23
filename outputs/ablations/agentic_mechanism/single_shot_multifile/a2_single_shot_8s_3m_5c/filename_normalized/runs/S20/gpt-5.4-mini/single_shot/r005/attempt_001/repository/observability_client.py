import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests


@dataclass
class ObservabilityClient:
    base_url: str
    api_key: str
    project_id: Optional[str] = None

    def _headers(self) -> Dict[str, str]:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        if self.project_id:
            headers["X-Project-Id"] = self.project_id
        return headers

    def write_log(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/v1/logs:write", headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def query_logs(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/v1/logs:query", headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()


def get_observability_client() -> ObservabilityClient:
    base_url = os.getenv("OBSERVABILITY_API_BASE_URL", "https://api.datadog.com")
    api_key = os.environ["DATADOG_API_KEY"]
    project_id = os.getenv("DATADOG_SITE")
    return ObservabilityClient(base_url=base_url, api_key=api_key, project_id=project_id)


def resolve_log_namespace() -> str:
    return os.getenv("OBSERVABILITY_LOG_NAMESPACE", "default")


def resolve_log_source(default: str) -> str:
    return os.getenv("OBSERVABILITY_LOG_SOURCE", default)