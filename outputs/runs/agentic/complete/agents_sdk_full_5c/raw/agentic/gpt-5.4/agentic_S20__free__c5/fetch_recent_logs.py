from __future__ import annotations

from typing import List, Optional

from observability_client import build_logs_list_request, default_time_range, ensure_required_credentials, get_logs_api
from observability_models import LogQueryRequest, NormalizedLogRecord, normalize_datadog_log


def fetch_recent_logs(service: str = "checkout-api", field: str = "@http.status_code", value: Optional[str] = None, minutes: int = 15, limit: int = 25) -> List[NormalizedLogRecord]:
    ensure_required_credentials(require_app_key=True)
    start, end = default_time_range(minutes)
    query = f"service:{service}"
    if value is not None:
        query += f" {field}:{value}"
    request = LogQueryRequest(query=query, from_time=start, to_time=end, limit=limit, sort="desc")
    response = get_logs_api().list_logs(body=build_logs_list_request(request))
    return [normalize_datadog_log(item.to_dict()) for item in response.data]
