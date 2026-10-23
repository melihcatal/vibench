import os
from typing import Any, Dict, Optional

import requests

from observability_models import (
    LogQuery,
    log_event_body,
    query_window,
    response_records,
)


class DatadogLogsClient:
    api_host = "https://http-intake.logs.datadoghq.com/api/v2/logs"
    search_host = "https://api.datadoghq.com/api/v2/logs/events/search"

    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("DD_API_KEY", "")
        self.app_key = app_key or os.getenv("DD_APP_KEY", "")
        self.site = site or os.getenv("DD_SITE", "datadoghq.com")

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def write_log(
        self,
        service: str,
        message: str,
        severity: str = "info",
        correlation_id: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = [
            log_event_body(
                service,
                message,
                severity=severity,
                correlation_id=correlation_id,
                fields=fields,
            )
        ]
        resp = requests.post(
            self.api_host, headers=self._headers(), json=payload, timeout=20
        )
        resp.raise_for_status()
        return {"status_code": resp.status_code, "body": resp.text or "accepted"}

    def query_logs(self, query: LogQuery) -> Dict[str, Any]:
        time_window = query_window(query.start_time, query.end_time)
        filter_parts = []
        if query.severity:
            filter_parts.append(f"@severity:{query.severity}")
        if query.text:
            filter_parts.append(f'"{query.text}"')
        if query.field_name and query.field_value is not None:
            filter_parts.append(f"@{query.field_name}:{query.field_value}")
        filter_query = " ".join(filter_parts) or "*"
        body = {
            "filter": {
                "from": time_window["start_time"],
                "to": time_window["end_time"],
                "query": filter_query,
            },
            "page": {"limit": 100},
        }
        resp = requests.post(
            self.search_host, headers=self._headers(), json=body, timeout=20
        )
        resp.raise_for_status()
        data = resp.json()
        return {"query": body, "records": response_records(data), "raw": data}


def client() -> DatadogLogsClient:
    return DatadogLogsClient()
