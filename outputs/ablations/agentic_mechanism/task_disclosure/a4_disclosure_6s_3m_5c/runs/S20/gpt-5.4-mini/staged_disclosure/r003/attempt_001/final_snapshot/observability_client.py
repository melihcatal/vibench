import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ManagedLogQueryConfig:
    api_key: str
    source_token: str
    base_url: str = "https://api.logtail.com"


def load_managed_log_query_config(prefix: str = "LOGTAIL") -> ManagedLogQueryConfig:
    api_key = os.getenv(f"{prefix}_SOURCE_TOKEN") or os.getenv("LOGTAIL_SOURCE_TOKEN")
    source_token = os.getenv(f"{prefix}_LOG_SOURCE_TOKEN") or os.getenv("LOGTAIL_LOG_SOURCE_TOKEN")
    if not api_key or not source_token:
        raise RuntimeError("LOGTAIL_SOURCE_TOKEN and LOGTAIL_LOG_SOURCE_TOKEN are required")
    return ManagedLogQueryConfig(api_key=api_key, source_token=source_token)


def _coerce_iso8601(value: Optional[str]) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _default_window_minutes() -> int:
    raw = os.getenv("LOGTAIL_WINDOW_MINUTES", "60")
    try:
        return max(1, int(raw))
    except ValueError:
        return 60


def build_log_query(severity: str, start: datetime, end: datetime) -> Dict[str, Any]:
    start_utc = start.astimezone(timezone.utc)
    end_utc = end.astimezone(timezone.utc)
    return {
        "query": f'severity:{severity} AND timestamp:["{start_utc.isoformat()}" TO "{end_utc.isoformat()}"]',
        "from": start_utc.isoformat(),
        "to": end_utc.isoformat(),
        "limit": 100,
    }


class ManagedLogClient:
    def __init__(self, config: Optional[ManagedLogQueryConfig] = None, session: Optional[requests.Session] = None) -> None:
        self.config = config or load_managed_log_query_config()
        self.session = session or requests.Session()

    def query_logs(self, severity: str = "error", start: Optional[datetime] = None, end: Optional[datetime] = None) -> Any:
        end_dt = end or datetime.now(timezone.utc)
        start_dt = start or (end_dt - timedelta(minutes=_default_window_minutes()))
        url = f"{self.config.base_url}/v1/sources/{self.config.source_token}/search"
        response = self.session.post(
            url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json=build_log_query(severity, start_dt, end_dt),
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("data", payload)

    def ingest_log(self, event_name: str, severity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.config.base_url}/v1/sources/{self.config.source_token}/ingest"
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_name": event_name,
            "severity": severity,
            "payload": payload,
            "provider": "logtail",
        }
        response = self.session.post(
            url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps([record]),
            timeout=10,
        )
        response.raise_for_status()
        return record


def query_managed_logs(severity: str = "error", start: Optional[str] = None, end: Optional[str] = None) -> Any:
    client = ManagedLogClient()
    return client.query_logs(severity=severity, start=_coerce_iso8601(start) if start else None, end=_coerce_iso8601(end) if end else None)


def ingest_managed_log(event_name: str, severity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    client = ManagedLogClient()
    return client.ingest_log(event_name=event_name, severity=severity, payload=payload)
