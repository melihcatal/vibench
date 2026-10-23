import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


GOOGLE_CLOUD_MONITORING_ENDPOINT = "https://monitoring.googleapis.com/v3"


def _access_token() -> str:
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN") or os.getenv("GCP_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing Google Cloud access token")
    return token


def _project_name(project_id: Optional[str]) -> str:
    resolved = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not resolved:
        raise ValueError("Missing Google Cloud project id")
    return f"projects/{resolved}"


def _parse_time(value: Optional[str]) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    text = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def filter_metric_dimensions(
    metric_type: str,
    *,
    project_id: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
    page_size: int = 100,
) -> List[Dict[str, Any]]:
    project = _project_name(project_id)
    end_dt = _parse_time(end_time)
    start_dt = _parse_time(start_time) if start_time else end_dt - timedelta(hours=1)

    filter_parts = [f'metric.type = "{metric_type}"']
    if resource_type:
        filter_parts.append(f'resource.type = "{resource_type}"')
    if resource_labels:
        for key, value in resource_labels.items():
            filter_parts.append(f'resource.labels."{key}" = "{value}"')
    if metric_labels:
        for key, value in metric_labels.items():
            filter_parts.append(f'metric.labels."{key}" = "{value}"')

    params = {
        "filter": " AND ".join(filter_parts),
        "interval.startTime": start_dt.isoformat().replace("+00:00", "Z"),
        "interval.endTime": end_dt.isoformat().replace("+00:00", "Z"),
        "pageSize": page_size,
    }

    headers = {"Authorization": f"Bearer {_access_token()}"}
    url = f"{GOOGLE_CLOUD_MONITORING_ENDPOINT}/{project}/timeSeries"
    results: List[Dict[str, Any]] = []

    while True:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        results.extend(payload.get("timeSeries", []))
        token = payload.get("nextPageToken")
        if not token:
            break
        params["pageToken"] = token

    return results
