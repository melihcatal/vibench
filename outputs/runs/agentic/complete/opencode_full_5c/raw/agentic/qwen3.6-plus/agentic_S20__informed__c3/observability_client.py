import os
import json
from typing import Optional
from datetime import datetime, timezone

import requests

DD_SITE = os.environ.get("DD_SITE", "datadoghq.com")
DD_API_KEY = os.environ["DD_API_KEY"]
DD_APP_KEY = os.environ.get("DD_APP_KEY", "")
DD_API_BASE_URL = f"https://api.{DD_SITE}/api/v2"
DD_LOGS_INGEST_URL = f"{DD_API_BASE_URL}/logs"
DD_LOGS_QUERY_URL = f"{DD_API_BASE_URL}/logs/events/search"


def build_dd_headers() -> dict:
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DD_API_KEY,
    }
    if DD_APP_KEY:
        headers["DD-APPLICATION-KEY"] = DD_APP_KEY
    return headers


def build_log_payload(
    message: str,
    level: str,
    service: str,
    source: str,
    correlation_id: Optional[str] = None,
    extra_attributes: Optional[dict] = None,
    timestamp: Optional[datetime] = None,
) -> dict:
    ts = timestamp or datetime.now(timezone.utc)
    ddtags = [f"service:{service}", f"source:{source}", f"level:{level}"]
    if correlation_id:
        ddtags.append(f"correlation_id:{correlation_id}")
    payload = {
        "ddsource": source,
        "ddtags": ",".join(ddtags),
        "hostname": os.environ.get("HOSTNAME", "unknown"),
        "message": message,
        "service": service,
        "status": level.upper(),
        "timestamp": int(ts.timestamp() * 1000),
    }
    if correlation_id:
        payload["correlation_id"] = correlation_id
    if extra_attributes:
        payload.update(extra_attributes)
    return payload


def ingest_logs(payloads: list[dict]) -> requests.Response:
    body = payloads if isinstance(payloads, list) else [payloads]
    return requests.post(
        DD_LOGS_INGEST_URL,
        headers=build_dd_headers(),
        json=body,
        timeout=30,
    )


def query_logs(
    query: str,
    start_time: datetime,
    end_time: datetime,
    limit: int = 50,
    sort: str = "timestamp",
) -> requests.Response:
    body = {
        "filter": {
            "query": query,
            "from": start_time.isoformat(),
            "to": end_time.isoformat(),
        },
        "page": {
            "limit": limit,
        },
        "sort": sort,
    }
    return requests.post(
        DD_LOGS_QUERY_URL,
        headers=build_dd_headers(),
        json=body,
        timeout=30,
    )


def parse_query_response(response: requests.Response) -> list[dict]:
    if response.status_code != 200:
        raise RuntimeError(
            f"Datadog query failed: {response.status_code} {response.text}"
        )
    data = response.json()
    events = data.get("data", [])
    results = []
    for event in events:
        attrs = event.get("attributes", {})
        results.append(
            {
                "id": event.get("id", ""),
                "timestamp": attrs.get("timestamp", ""),
                "message": attrs.get("message", ""),
                "status": attrs.get("status", ""),
                "service": attrs.get("service", ""),
                "tags": attrs.get("tags", []),
                "attributes": attrs,
            }
        )
    return results
