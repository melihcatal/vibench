"""
fetch_recent_logs.py

Retrieves recent log results from Amazon CloudWatch Logs Insights
filtered by field values and time range using the boto3 SDK.
"""

import os
import time
from typing import Optional
from observability_client import get_cloudwatch_logs_client, build_time_filter
from observability_models import (
    LogQueryResult,
    QueryResponse,
    build_field_filter_query,
)


def fetch_recent_logs(
    log_group_name: str,
    field_name: str,
    field_value: str,
    hours_back: int = 1,
    limit: int = 100,
) -> QueryResponse:
    """
    Fetch recent CloudWatch log entries filtered by a specific field
    and value within a time window.

    Args:
        log_group_name: CloudWatch log group to search.
        field_name: The structured field to filter on (e.g. 'service').
        field_value: The value to match for the field.
        hours_back: Look-back window in hours.
        limit: Maximum number of result rows.

    Returns:
        QueryResponse containing the matching log entries.
    """
    client = get_cloudwatch_logs_client()
    start_ms, end_ms = build_time_filter(hours_back=hours_back)

    query_string = build_field_filter_query(
        field_name=field_name,
        field_value=field_value,
        hours_back=hours_back,
        limit=limit,
    )

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

    stats = status_resp.get("statistics", {})
    total = stats.get("recordsMatched", 0)

    return QueryResponse(results=results, total_matches=total)


if __name__ == "__main__":
    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    resp = fetch_recent_logs(
        log_group_name=lg,
        field_name="service",
        field_value="payment-api",
        hours_back=6,
        limit=50,
    )
    print(resp.to_json())
