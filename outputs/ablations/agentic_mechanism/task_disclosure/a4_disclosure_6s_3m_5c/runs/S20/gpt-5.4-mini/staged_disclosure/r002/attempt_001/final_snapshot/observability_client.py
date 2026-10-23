import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


SPLUNK_API_BASE_URL = os.getenv("SPLUNK_API_BASE_URL", "https://api.splunk.com")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN", "")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc(dt: Optional[datetime]) -> datetime:
    if dt is None:
        return _utc_now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _isoformat_utc(dt: datetime) -> str:
    return _to_utc(dt).isoformat().replace("+00:00", "Z")


def _require_token() -> str:
    if not SPLUNK_TOKEN:
        raise ValueError("SPLUNK_TOKEN is required")
    return SPLUNK_TOKEN


@dataclass(frozen=True)
class LogQueryConfig:
    base_url: str = SPLUNK_API_BASE_URL
    token: str = SPLUNK_TOKEN
    default_window_hours: int = 1
    request_timeout_seconds: int = 30

    @classmethod
    def from_env(cls) -> "LogQueryConfig":
        return cls(
            base_url=os.getenv("SPLUNK_API_BASE_URL", SPLUNK_API_BASE_URL),
            token=os.getenv("SPLUNK_TOKEN", SPLUNK_TOKEN),
            default_window_hours=int(os.getenv("LOG_QUERY_WINDOW_HOURS", "1")),
            request_timeout_seconds=int(os.getenv("LOG_QUERY_TIMEOUT_SECONDS", "30")),
        )


class ManagedLogClient:
    def __init__(self, config: Optional[LogQueryConfig] = None) -> None:
        self.config = config or LogQueryConfig.from_env()

    def _auth_headers(self) -> Dict[str, str]:
        if not self.config.token:
            raise ValueError("SPLUNK_TOKEN is required")
        return {"Authorization": f"Bearer {self.config.token}"}

    def query_logs(
        self,
        field_filters: Optional[Dict[str, Any]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        end_time_utc = _to_utc(end_time) if end_time else _utc_now()
        start_time_utc = _to_utc(start_time) if start_time else end_time_utc - timedelta(hours=self.config.default_window_hours)
        query_parts = [f'{k}="{v}"' for k, v in (field_filters or {}).items()]
        query = " AND ".join(query_parts) if query_parts else "*"
        params = {
            "query": query,
            "start_time": _isoformat_utc(start_time_utc),
            "end_time": _isoformat_utc(end_time_utc),
            "limit": limit,
        }
        response = requests.get(
            f"{self.config.base_url.rstrip('/')}/v1/search/logs",
            headers=self._auth_headers(),
            params=params,
            timeout=self.config.request_timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        if isinstance(data, list):
            return data
        return []

    def ingest_logs(self, records: Iterable[Dict[str, Any]]) -> int:
        payload = list(records)
        if not payload:
            return 0
        response = requests.post(
            f"{self.config.base_url.rstrip('/')}/v1/ingest/logs",
            headers={**self._auth_headers(), "Content-Type": "application/json"},
            json={"records": payload},
            timeout=self.config.request_timeout_seconds,
        )
        response.raise_for_status()
        return len(payload)


def get_client() -> ManagedLogClient:
    return ManagedLogClient()


def query_recent_logs(field_filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    return get_client().query_logs(field_filters=field_filters, limit=limit)


def ingest_structured_log(message: str, **fields: Any) -> int:
    record = {
        "message": message,
        "timestamp": _isoformat_utc(_utc_now()),
        "service": fields.pop("service", "observability-client"),
        **fields,
    }
    return get_client().ingest_logs([record])


if __name__ == "__main__":
    client = get_client()
    print(client.query_logs({"service": "api", "level": "error"}, limit=10))
