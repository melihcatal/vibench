import requests
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


def fetch_recent_logs(
    field_filters: Dict[str, str], time_range_hours: int = 1
) -> List[Dict[str, Any]]:
    api_key = os.getenv("DATADOG_API_KEY")
    app_key = os.getenv("DATADOG_APP_KEY")
    if not api_key or not app_key:
        return []
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=time_range_hours)).timestamp() * 1000)
    url = "https://api.datadoghq.com/api/v2/logs/queries/list"
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }
    query_parts = [f"{k}:{v}" for k, v in field_filters.items()]
    query_str = " ".join(query_parts)
    body = {
        "queries": [{"query": query_str, "time": {"from": from_ts, "to": to_ts}}],
        "page": {"limit": 1000},
    }
    resp = requests.post(url, headers=headers, json=body)
    if resp.status_code != 200:
        return []
    data = resp.json()
    logs = []
    if "data" in data and data["data"]:
        qr = data["data"][0]
        if "logs" in qr:
            logs = [entry.get("attributes", {}) for entry in qr["logs"]]
    return logs
