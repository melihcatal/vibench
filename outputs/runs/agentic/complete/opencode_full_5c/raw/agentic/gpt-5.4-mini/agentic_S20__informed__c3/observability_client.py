import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass(frozen=True)
class DatadogConfig:
    site: str
    api_key: str
    app_key: str
    service: str
    source: str


def load_config() -> DatadogConfig:
    site = os.getenv("DD_SITE", "datadoghq.com")
    api_key = os.environ["DD_API_KEY"]
    app_key = os.environ["DD_APP_KEY"]
    service = os.getenv("DD_SERVICE", "observability-demo")
    source = os.getenv("DD_SOURCE", "python")
    return DatadogConfig(
        site=site, api_key=api_key, app_key=app_key, service=service, source=source
    )


def _base_url(site: str) -> str:
    return f"https://api.{site}"


def _headers(cfg: DatadogConfig) -> Dict[str, str]:
    return {
        "DD-API-KEY": cfg.api_key,
        "DD-APPLICATION-KEY": cfg.app_key,
        "Content-Type": "application/json",
    }


def ingest_log(
    event: Dict[str, Any], cfg: Optional[DatadogConfig] = None
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    payload = [event]
    resp = requests.post(
        f"{_base_url(cfg.site)}/api/v2/logs",
        headers=_headers(cfg),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return {"status_code": resp.status_code, "response_text": resp.text}


def query_logs(
    filter_query: str,
    start: datetime,
    end: datetime,
    cfg: Optional[DatadogConfig] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    payload = {
        "filter": {
            "query": filter_query,
            "from": start.astimezone(timezone.utc).isoformat(),
            "to": end.astimezone(timezone.utc).isoformat(),
        },
        "page": {"limit": limit},
        "sort": "timestamp",
    }
    resp = requests.post(
        f"{_base_url(cfg.site)}/api/v2/logs/events/search",
        headers=_headers(cfg),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
