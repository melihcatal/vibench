import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, QueryResult, normalize_log_event

DATADOG_API_HOST = "https://api.datadoghq.com"


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_key: str
    site: str = DATADOG_API_HOST

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }


def load_config() -> DatadogConfig:
    api_key = os.environ.get("DD_API_KEY", "")
    app_key = os.environ.get("DD_APP_KEY", "")
    if not api_key or not app_key:
        raise EnvironmentError("DD_API_KEY and DD_APP_KEY are required for Datadog Logs API access")
    return DatadogConfig(api_key=api_key, app_key=app_key)


def _session(config: Optional[DatadogConfig] = None) -> requests.Session:
    config = config or load_config()
    session = requests.Session()
    session.headers.update(config.headers)
    session.headers["DD-API-KEY"] = config.api_key
    session.headers["DD-APPLICATION-KEY"] = config.app_key
    return session


def ingest_log(event: LogEvent, config: Optional[DatadogConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    session = _session(cfg)
    payload = normalize_log_event(event)
    response = session.post(f"{cfg.site}/api/v2/logs", json=[payload], timeout=30)
    response.raise_for_status()
    return response.json() if response.content else {"status": "accepted"}


def query_logs(query: str, start: datetime, end: datetime, limit: int = 50, config: Optional[DatadogConfig] = None) -> QueryResult:
    cfg = config or load_config()
    session = _session(cfg)
    payload = {
        "filter": {
            "query": query,
            "from": start.astimezone(timezone.utc).isoformat(),
            "to": end.astimezone(timezone.utc).isoformat(),
        },
        "page": {"limit": limit},
        "sort": "timestamp",
    }
    response = session.post(f"{cfg.site}/api/v2/logs/events/search", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return QueryResult.from_datadog(data)


def recent_time_range(minutes: int = 15) -> tuple[datetime, datetime]:
    end = datetime.now(timezone.utc)
    return end - timedelta(minutes=minutes), end
