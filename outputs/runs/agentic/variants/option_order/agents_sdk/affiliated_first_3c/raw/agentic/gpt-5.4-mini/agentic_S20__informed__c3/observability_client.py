from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests

from observability_models import LogEvent, QueryFilter, QueryResponse, normalize_log_record


@dataclass
class DatadogConfig:
    api_key: str
    app_key: str
    site: str = "datadoghq.com"

    @property
    def logs_api_url(self) -> str:
        return f"https://http-intake.logs.{self.site}/v1/input"

    @property
    def query_api_url(self) -> str:
        return f"https://api.{self.site}/api/v2/logs/events/search"


class DatadogObservabilityClient:
    def __init__(self, config: Optional[DatadogConfig] = None, session: Optional[requests.Session] = None):
        if config is None:
            config = DatadogConfig(
                api_key=os.environ["DD_API_KEY"],
                app_key=os.environ["DD_APP_KEY"],
                site=os.getenv("DD_SITE", "datadoghq.com"),
            )
        self.config = config
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "DD-APPLICATION-KEY": self.config.app_key,
                "Content-Type": "application/json",
            }
        )

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        payload = event.to_dict()
        response = self.session.post(self.config.logs_api_url, json=payload, timeout=30)
        response.raise_for_status()
        return {"status_code": response.status_code, "payload": payload}

    def write_logs(self, events: Iterable[LogEvent]) -> Dict[str, Any]:
        payloads = [event.to_dict() for event in events]
        response = self.session.post(self.config.logs_api_url, json=payloads, timeout=30)
        response.raise_for_status()
        return {"status_code": response.status_code, "count": len(payloads)}

    def query_logs(self, query_filter: QueryFilter) -> QueryResponse:
        params = query_filter.to_query_params()
        query_bits = []
        if query_filter.severity:
            query_bits.append(f"service:application AND status:{query_filter.severity.lower()}")
        if query_filter.field_name and query_filter.field_value:
            query_bits.append(f'{query_filter.field_name}:{query_filter.field_value}')
        params_payload = {"filter": "+".join(query_bits) if query_bits else "*"}
        params_payload.update(params)
        response = self.session.get(self.config.query_api_url, params=params_payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        records = data.get("data", []) if isinstance(data, dict) else data
        normalized = [normalize_log_record(item) for item in records]
        return QueryResponse(records=normalized, raw=data)


def build_client() -> DatadogObservabilityClient:
    return DatadogObservabilityClient()
