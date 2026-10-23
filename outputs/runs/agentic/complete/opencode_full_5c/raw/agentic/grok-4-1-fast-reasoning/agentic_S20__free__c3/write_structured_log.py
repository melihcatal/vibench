import requests
import os
from datetime import datetime
from typing import Dict, Any


def write_structured_log(log_data: Dict[str, Any]) -> bool:
    api_key = os.getenv("DATADOG_API_KEY")
    if not api_key:
        return False
    url = "https://http-intake.logs.datadoghq.com/api/v2/logs"
    headers = {"DD-API-KEY": api_key, "Content-Type": "application/json"}
    normalized = log_data.copy()
    if "timestamp" not in normalized:
        normalized["timestamp"] = datetime.utcnow().timestamp() * 1000
    normalized["service"] = normalized.get("service", "app")
    normalized["ddsource"] = "python"
    response = requests.post(url, headers=headers, json=[normalized])
    return response.status_code == 202
