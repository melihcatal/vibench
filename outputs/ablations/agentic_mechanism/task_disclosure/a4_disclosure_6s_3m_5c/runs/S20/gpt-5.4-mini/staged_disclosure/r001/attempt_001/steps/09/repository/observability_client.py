import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


GRAFANA_LOKI_QUERY_RANGE_URL = os.environ.get(
    "GRAFANA_LOKI_QUERY_RANGE_URL",
    "https://logs-prod-us.grafana.net/loki/api/v1/query_range",
)
GRAFANA_LOKI_PUSH_URL = os.environ.get(
    "GRAFANA_LOKI_PUSH_URL",
    "https://logs-prod-us.grafana.net/loki/api/v1/push",
)


@dataclass(frozen=True)
class ManagedLogConfig:
    username: str
    api_key: str
    query_range_url: str = GRAFANA_LOKI_QUERY_RANGE_URL
    push_url: str = GRAFANA_LOKI_PUSH_URL


def _load_config() -> ManagedLogConfig:
    username = os.environ.get("GRAFANA_CLOUD_LOGS_USERNAME")
    api_key = os.environ.get("GRAFANA_CLOUD_API_KEY")
    if not username or not api_key:
        raise RuntimeError("GRAFANA_CLOUD_LOGS_USERNAME and GRAFANA_CLOUD_API_KEY are required")
    return ManagedLogConfig(username=username, api_key=api_key)


def _parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _to_ns(dt: datetime) -> int:
    return int(dt.timestamp() * 1_000_000_000)


def build_loki_label_query(filters: Optional[Dict[str, Any]] = None) -> str:
    filters = filters or {}
    if not filters:
        return "{}"
    parts = [f'{key}="{value}"' for key, value in filters.items()]
    return "{" + ",".join(parts) + "}"


def query_logs(
    query: str,
    start_time: str,
    end_time: str,
    limit: int = 100,
    step: Optional[str] = None,
) -> Dict[str, Any]:
    config = _load_config()
    params: Dict[str, Any] = {
        "query": query,
        "start": _to_ns(_parse_time(start_time)),
        "end": _to_ns(_parse_time(end_time)),
        "limit": int(limit),
    }
    if step is not None:
        params["step"] = step
    response = requests.get(
        config.query_range_url,
        params=params,
        auth=(config.username, config.api_key),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def query_logs_by_labels(
    labels: Optional[Dict[str, Any]],
    start_time: str,
    end_time: str,
    limit: int = 100,
) -> Dict[str, Any]:
    return query_logs(build_loki_label_query(labels), start_time, end_time, limit=limit)


def ingest_logs(entries: Iterable[Dict[str, Any]], stream_labels: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    config = _load_config()
    stream_labels = stream_labels or {}
    values: List[List[str]] = []
    for entry in entries:
        timestamp = entry.get("timestamp") or entry.get("ts") or datetime.now(timezone.utc)
        if isinstance(timestamp, str):
            timestamp = _parse_time(timestamp)
        if not isinstance(timestamp, datetime):
            raise TypeError("Each log entry timestamp must be a datetime or ISO-8601 string")
        payload = dict(entry)
        payload.pop("timestamp", None)
        payload.pop("ts", None)
        values.append([str(_to_ns(timestamp.astimezone(timezone.utc))), json.dumps(payload, separators=(",", ":"), sort_keys=True)])
    body = {"streams": [{"stream": stream_labels, "values": values}]}
    response = requests.post(
        config.push_url,
        auth=(config.username, config.api_key),
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    return {"status_code": response.status_code}


def get_client_config() -> ManagedLogConfig:
    return _load_config()
