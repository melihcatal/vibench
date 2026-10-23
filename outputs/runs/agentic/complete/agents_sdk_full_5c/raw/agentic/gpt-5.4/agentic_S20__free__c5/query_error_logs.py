from __future__ import annotations

from typing import List

from observability_client import build_logs_list_request, default_time_range, ensure_required_credentials, get_logs_api
from observability_models import LogQueryRequest, NormalizedLogRecord, normalize_datadog_log


def query_error_logs(service: str = "checkout-api", minutes: int = 30, limit: int = 20) -> List[NormalizedLogRecord]:
    ensure_required_credentials(require_app_key=True)
    start, end = default_time_range(minutes)
    request = LogQueryRequest(
        query=f"service:{service} status:error",
        from_time=start,
        to_time=end,
        limit=limit,
        sort="desc",
    )
    response = get_logs_api().list_logs(body=build_logs_list_request(request))
    return [normalize_datadog_log(item.to_dict()) for item in response.data]
