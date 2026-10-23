import requests
import os
from datetime import datetime
from typing import List, Dict, Any


def write_correlated_logs(
    correlation_id: str, log_events: List[Dict[str, Any]]
) -> bool:
    api_key = os.getenv("DATADOG_API_KEY")
    if not api_key:
        return False
    url = "https://http-intake.logs.datadoghq.com/api/v2/logs"
    headers = {"DD-API-KEY": api_key, "Content-Type": "application/json"}
    normalized_logs = []
    for event in log_events:
        norm = event.copy()
        norm["correlation_id"] = correlation_id
        if "timestamp" not in norm:
            norm["timestamp"] = datetime.utcnow().timestamp() * 1000
        norm["service"] = norm.get("service", "app")
        norm["ddsource"] = "python"
        normalized_logs.append(norm)
    response = requests.post(url, headers=headers, json=normalized_logs)
    return response.status_code == 202
