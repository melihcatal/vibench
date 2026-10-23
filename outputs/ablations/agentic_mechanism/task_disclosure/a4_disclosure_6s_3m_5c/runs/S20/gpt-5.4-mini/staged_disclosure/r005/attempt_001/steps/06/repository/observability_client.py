import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


GOOGLE_LOGGING_API_BASE = "https://logging.googleapis.com/v2"


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    api_key: str
    service_name: str = "google_cloud_logging"

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
        service_name = os.getenv("CLOUD_LOGGING_SERVICE", "google_cloud_logging")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_PROJECT_ID is required")
        if not api_key:
            raise ValueError("GOOGLE_CLOUD_API_KEY is required")
        return cls(project_id=project_id, api_key=api_key, service_name=service_name)


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None, timeout: int = 30):
        self.config = config or ObservabilityConfig.from_env()
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{GOOGLE_LOGGING_API_BASE}/projects/{self.config.project_id}/{path}"
        response = self.session.post(
            url,
            params={"key": self.config.api_key},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json() if response.content else {}

    @staticmethod
    def _format_timestamp(value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _build_filter(start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, field_filters: Optional[Dict[str, str]] = None, severity: Optional[str] = None) -> str:
        clauses: List[str] = []
        if start_time is not None:
            clauses.append(f'timestamp >= "{ObservabilityClient._format_timestamp(start_time)}"')
        if end_time is not None:
            clauses.append(f'timestamp <= "{ObservabilityClient._format_timestamp(end_time)}"')
        if severity:
            clauses.append(f"severity >= {severity}")
        for key, value in (field_filters or {}).items():
            clauses.append(f'jsonPayload.{key} = "{value}"')
        return " AND ".join(clauses)

    def write_structured_log(self, message: str, severity: str = "INFO", **fields: Any) -> Dict[str, Any]:
        event = {
            "entries": [
                {
                    "jsonPayload": {
                        "service": self.config.service_name,
                        "message": message,
                        "severity": severity,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        **fields,
                    }
                }
            ]
        }
        return self._request("entries:write", event)

    def fetch_recent_logs(self, hours: int = 24, limit: int = 100, field_filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours)
        payload = {
            "filter": self._build_filter(start_time=start_time, end_time=end_time, field_filters=field_filters),
            "orderBy": "timestamp desc",
            "pageSize": limit,
        }
        return self._request("entries:list", payload).get("entries", [])

    def query_error_logs(self, severity: str = "ERROR", hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours)
        payload = {
            "filter": self._build_filter(start_time=start_time, end_time=end_time, severity=severity),
            "orderBy": "timestamp desc",
            "pageSize": limit,
        }
        return self._request("entries:list", payload).get("entries", [])


def load_observability_config() -> ObservabilityConfig:
    return ObservabilityConfig.from_env()


def get_observability_client(timeout: int = 30) -> ObservabilityClient:
    return ObservabilityClient(timeout=timeout)
