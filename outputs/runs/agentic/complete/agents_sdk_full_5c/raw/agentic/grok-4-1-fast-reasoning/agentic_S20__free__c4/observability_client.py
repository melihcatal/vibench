import os
import gzip
import json
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta

from observability_models import LogEvent, LogsQueryParams

DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
if not DATADOG_API_KEY:
    raise ValueError("DATADOG_API_KEY environment variable is required.")

INTAKE_URL = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"
SEARCH_URL = f"https://api.{DATADOG_SITE}/api/v2/logs/queries/list"

COMMON_HEADERS = {
    "DD-API-KEY": DATADOG_API_KEY,
}

def write_log(event: LogEvent) -> bool:
    payload = event.datadog_payload()
    body = gzip.compress(json.dumps(payload).encode("utf-8"))
    headers = COMMON_HEADERS.copy()
    headers.update({
        "Content-Type": "application/json",
        "Content-Encoding": "gzip",
    })
    resp = requests.post(INTAKE_URL, data=body, headers=headers)
    return 202 <= resp.status_code < 300

def write_logs(events: List[LogEvent]) -> bool:
    return all(write_log(event) for event in events)

def query_logs(params: LogsQueryParams) -> Dict[str, Any]:
    headers = COMMON_HEADERS.copy()
    headers["Content-Type"] = "application/json"
    resp = requests.post(SEARCH_URL, json=params.dict(by_alias=True), headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_recent_errors(service: str = "myapp", minutes: int = 60) -> Dict[str, Any]:
    now = datetime.utcnow()
    from_ts = int((now - timedelta(minutes=minutes)).timestamp() * 1000)
    to_ts = int(now.timestamp() * 1000)
    params = LogsQueryParams(
        query=f"service:{service} @severity:ERROR",
        time={"from": from_ts, "to": to_ts}
    )
    return query_logs(params)