import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, QueryRequest, QueryResult, isoformat_utc


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("DD_API_KEY")
        self.app_key = app_key or os.getenv("DD_APP_KEY")
        self.site = site or os.getenv("DD_SITE", "datadoghq.com")
        self.base_url = f"https://api.{self.site}"

    def headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key or "",
            "DD-APPLICATION-KEY": self.app_key or "",
            "Content-Type": "application/json",
        }

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/v2/logs",
            headers=self.headers(),
            json=[event.to_dict()],
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.content else {"status": "ok"}

    def query_logs(self, request: QueryRequest) -> QueryResult:
        query = [f"@severity:{request.severity}"] if request.severity else []
        for key, value in request.field_filters.items():
            query.append(f"@{key}:{value}")
        query_str = " AND ".join(query) if query else "*"
        payload = {
            "filter": {
                "from": request.start_time,
                "to": request.end_time,
                "query": query_str,
            },
            "page": {"limit": request.limit},
        }
        response = requests.post(
            f"{self.base_url}/api/v2/logs/events/search",
            headers=self.headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        items = [item.get("attributes", {}) for item in data.get("data", [])]
        return QueryResult(
            items=items, next_token=data.get("meta", {}).get("page", {}).get("after")
        )


def default_time_window(minutes: int = 15) -> tuple[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return isoformat_utc(start), isoformat_utc(end)
