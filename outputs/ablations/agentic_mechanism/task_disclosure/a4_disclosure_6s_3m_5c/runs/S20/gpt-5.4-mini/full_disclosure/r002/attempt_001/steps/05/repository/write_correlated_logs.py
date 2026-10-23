import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


class DatadogLogsClient:
    def __init__(self, api_key: Optional[str] = None, site: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("DD_API_KEY")
        self.site = site or os.getenv("DD_SITE", "datadoghq.com")
        if not self.api_key:
            raise ValueError("DD_API_KEY is required")

    def submit_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"https://http-intake.logs.{self.site}/api/v2/logs"
        headers = {
            "DD-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=json.dumps(logs), timeout=30)
        response.raise_for_status()
        return {"status_code": response.status_code, "accepted": True}


def write_correlated_logs(
    request_id: str,
    messages: List[str],
    service: str = "application-service",
    environment: str = "production",
    level: str = "info",
    api_key: Optional[str] = None,
    site: Optional[str] = None,
) -> Dict[str, Any]:
    client = DatadogLogsClient(api_key=api_key, site=site)
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = []
    for index, message in enumerate(messages):
        payload.append(
            {
                "message": message,
                "ddsource": "python",
                "service": service,
                "ddtags": f"env:{environment}",
                "status": level,
                "timestamp": timestamp,
                "correlation_id": request_id,
                "request_id": request_id,
                "event_index": index,
            }
        )
    return client.submit_logs(payload)
