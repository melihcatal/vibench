"""
query_error_logs.py

Queries recent error log entries from Amazon CloudWatch Logs Insights,
filtered by severity and time range.
"""

import os
import time
from typing import List, Optional
from observability_client import get_cloudwatch_logs_client, build_time_filter
from observability_models import (
    LogQueryResult,
    QueryResponse,
    build_error_query,
)


def query_error_logs(
    log_group_name: str,
    hours_back: int = 1,
    log_level_filter: str = "ERROR",
    extra_filters: Optional[List[str]] = None,
    limit: int = 200,
) -> QueryResponse:
    """
    Query Amazon CloudWatch Logs Insights for recent error-level logs.

    Args:
        log_group_name: CloudWatch log group to search.
        hours_back: Look-back window in hours.
        log_level_filter: Severity value to filter on.
        extra_filters: Additional CloudWatch filter expressions.
        limit: Maximum number of results.

    Returns:
        QueryResponse with parsed LogQueryResult entries.
    """
    client = get_cloudwatch_logs_client()
    start_ms, end_ms = build_time_filter(hours_back=hours_back)

    query_string = build_error_query(
        hours_back=hours_back,
        log_level_filter=log_level_filter,
        extra_filters=extra_filters,
        limit=limit,
    )

    # Start the Insights query
    start_resp = client.start_query(
        logGroupName=log_group_name,
        startTime=start_ms,
        endTime=end_ms,
        queryString=query_string,
        limit=limit,
    )
    query_id = start_resp["queryId"]

    # Poll for results
    max_wait = 30
    waited = 0
    while waited < max_wait:
        time.sleep(2)
        waited += 2
        status_resp = client.get_query_results(queryId=query_id)
        status = status_resp["status"]
        if status in ("Complete", "Failed", "Cancelled"):
            break

    if status_resp["status"] != "Complete":
        return QueryResponse(results=[], total_matches=0)

    results = []
    for row in status_resp.get("results", []):
        record = LogQueryResult.from_cloudwatch_record(row)
        results.append(record)

    # Stats
    stats = status_resp.get("statistics", {})
    total = stats.get("recordsMatched", 0)

    return QueryResponse(results=results, total_matches=total)


if __name__ == "__main__":
    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    resp = query_error_logs(
        log_group_name=lg,
        hours_back=2,
        log_level_filter="ERROR",
        limit=50,
    )
    print(resp.to_json())
