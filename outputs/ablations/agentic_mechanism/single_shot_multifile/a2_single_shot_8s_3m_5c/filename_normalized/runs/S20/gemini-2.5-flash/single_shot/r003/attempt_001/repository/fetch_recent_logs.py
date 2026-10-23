from observability_client import clients
from observability_models import LogQueryResult
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort
from datadog_api_client.v2.model.content_encoding import ContentEncoding

def fetch_recent_logs(
    query_string: str,
    time_range_seconds: int = 3600,
    limit: int = 100
) -> List[LogQueryResult]:
    """
    Retrieves recent log results from Datadog, filtered by query string and time range.
    """
    datadog_logs_api = clients.datadog_logs_api

    now = datetime.utcnow()
    start_time = now - timedelta(seconds=time_range_seconds)

    query_filter = LogsQueryFilter(
        query=query_string,
        _from=start_time.isoformat("T") + "Z",
        to=now.isoformat("T") + "Z",
        indexes=["main"]
    )

    request = LogsListRequest(
        filter=query_filter,
        page={"limit": limit},
        sort=LogsSort.TIMESTAMP_DESCENDING
    )

    response = datadog_logs_api.list_logs(body=request)
    
    results: List[LogQueryResult] = []
    for log_entry in response.data:
        attributes = log_entry.attributes
        if attributes:
            message = attributes.message
            timestamp = attributes.timestamp
            service = attributes.service if hasattr(attributes, 'service') else "unknown"
            host = attributes.host if hasattr(attributes, 'host') else "unknown"
            status = attributes.status if hasattr(attributes, 'status') else "info"

            payload_data = attributes.to_dict()
            payload_data.pop("message", None)
            payload_data.pop("timestamp", None)
            payload_data.pop("status", None)
            payload_data.pop("service", None)
            payload_data.pop("host", None)

            results.append(
                LogQueryResult(
                    timestamp=timestamp,
                    severity=status.upper(),
                    message=message,
                    payload=payload_data,
                    log_name=service,
                    resource={"type": "host", "labels": {"host_name": host}},
                    trace_id=attributes.trace_id if hasattr(attributes, 'trace_id') else None,
                    span_id=attributes.span_id if hasattr(attributes, 'span_id') else None,
                )
            )
    return results
