from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.http_log_items import HTTPLogItems
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_query_options import LogsQueryOptions
from datadog_api_client.v2.model.logs_sort import LogsSort

from observability_models import StructuredLogEvent, ensure_json_line, normalize_datadog_log


DATADOG_SITE = os.getenv("DD_SITE", "datadoghq.com")
DATADOG_API_KEY = os.getenv("DD_API_KEY")
DATADOG_APP_KEY = os.getenv("DD_APP_KEY")
DATADOG_LOGS_HTTP_URL = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"


class DatadogObservabilityClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, site: Optional[str] = None) -> None:
        self.api_key = api_key or DATADOG_API_KEY
        self.app_key = app_key or DATADOG_APP_KEY
        self.site = site or DATADOG_SITE
        if not self.api_key:
            raise ValueError("DD_API_KEY is required for Datadog log ingestion")
        self._configuration = Configuration()
        self._configuration.server_variables["site"] = self.site
        self._configuration.api_key["apiKeyAuth"] = self.api_key
        if self.app_key:
            self._configuration.api_key["appKeyAuth"] = self.app_key

    def api_client(self) -> ApiClient:
        return ApiClient(self._configuration)

    def send_log(self, event: StructuredLogEvent) -> Any:
        body = HTTPLog([
            HTTPLogItem(ddsource="python", ddtags=f"service:{event.service},severity:{event.severity.lower()}", hostname="localhost", message=ensure_json_line(event), service=event.service)
        ])
        with self.api_client() as client:
            api = LogsApi(client)
            return api.submit_log(body=body, content_encoding="gzip")

    def send_logs(self, events: List[StructuredLogEvent]) -> Any:
        items = []
        for event in events:
            items.append(
                HTTPLogItem(
                    ddsource="python",
                    ddtags=f"service:{event.service},correlation_id:{event.correlation_id or 'none'},severity:{event.severity.lower()}",
                    hostname="localhost",
                    message=ensure_json_line(event),
                    service=event.service,
                )
            )
        body = HTTPLog(items)
        with self.api_client() as client:
            api = LogsApi(client)
            return api.submit_log(body=body, content_encoding="gzip")

    def list_logs(self, query: str, start: datetime, end: datetime, limit: int = 50) -> List[Dict[str, Any]]:
        if not self.app_key:
            raise ValueError("DD_APP_KEY is required for Datadog log queries")
        request = LogsListRequest(
            filter=LogsQueryFilter(
                _from=start.astimezone(timezone.utc).isoformat(),
                to=end.astimezone(timezone.utc).isoformat(),
                query=query,
            ),
            sort=LogsSort.TIMESTAMP_DESCENDING,
            page=LogsListRequestPage(limit=limit),
            options=LogsQueryOptions(timezone="UTC"),
        )
        with self.api_client() as client:
            api = LogsApi(client)
            response = api.list_logs(body=request)
            return [normalize_datadog_log(item.to_dict()).raw if hasattr(item, 'to_dict') else normalize_datadog_log(item).raw for item in response.data]


def default_time_range(minutes: int = 15) -> Dict[str, datetime]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return {"start": start, "end": end}
