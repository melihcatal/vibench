import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


LOGTAIL_BASE_URL = os.getenv("LOGTAIL_BASE_URL", "https://api.logtail.com")


@dataclass(frozen=True)
class ObservabilityConfig:
    source_token: str
    api_token: str
    base_url: str = LOGTAIL_BASE_URL


def load_config() -> ObservabilityConfig:
    source_token = os.getenv("LOGTAIL_SOURCE_TOKEN")
    api_token = os.getenv("LOGTAIL_API_TOKEN")
    base_url = os.getenv("LOGTAIL_BASE_URL", LOGTAIL_BASE_URL)
    if not source_token or not api_token:
        raise RuntimeError("LOGTAIL_SOURCE_TOKEN and LOGTAIL_API_TOKEN are required")
    return ObservabilityConfig(source_token=source_token, api_token=api_token, base_url=base_url)


def _session(api_token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"})
    return session


def _normalize_items(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        items = payload.get("data", payload.get("logs", payload.get("items", [])))
        return items if isinstance(items, list) else []
    if isinstance(payload, list):
        return payload
    return []


def query_logs(field_filters: Optional[Dict[str, Any]] = None, start_time: Optional[float] = None, end_time: Optional[float] = None, limit: int = 100, config: Optional[ObservabilityConfig] = None) -> List[Dict[str, Any]]:
    cfg = config or load_config()
    params: Dict[str, Any] = {"limit": limit}
    if start_time is not None:
        params["start"] = int(start_time)
    if end_time is not None:
        params["end"] = int(end_time)
    if field_filters:
        params.update(field_filters)
    response = requests.get(f"{cfg.base_url}/sources/{cfg.source_token}/logs", headers={"Authorization": f"Bearer {cfg.api_token}"}, params=params, timeout=30)
    response.raise_for_status()
    return _normalize_items(response.json())


def _to_iso8601(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def ingest_log(message: str, level: str = "info", fields: Optional[Dict[str, Any]] = None, timestamp: Optional[datetime] = None, config: Optional[ObservabilityConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    payload: Dict[str, Any] = {"message": message, "level": level, "timestamp": _to_iso8601(timestamp) or datetime.now(timezone.utc).isoformat()}
    if fields:
        payload.update(fields)
    response = _session(cfg.api_token).post(f"{cfg.base_url}/sources/{cfg.source_token}/logs", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {"status": "ok", "response": data}


def ingest_logs(entries: Iterable[Dict[str, Any]], config: Optional[ObservabilityConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    response = _session(cfg.api_token).post(f"{cfg.base_url}/sources/{cfg.source_token}/logs", json={"logs": list(entries)}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {"status": "ok", "response": data}
