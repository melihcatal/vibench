import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from observability_client import get_aws_cloudwatch_client
from observability_models import QueryResults


def query_error_logs(
    log_group_name: str,
    severity: str = "ERROR",
    duration_minutes: int = 60,
    region_name: Optional[str] = None,
) -> QueryResults:
    client = get_aws_cloudwatch_client(region_name or os.environ.get("AWS_REGION", "us-east-1"))

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    query_string = (
        f"fields @timestamp, @message | filter severity = '{severity}' | sort @timestamp desc"
    )

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        queryString=query_string,
        limit=100  # Limiting to 100 results for demonstration
    )

    query_id = start_query_response["queryId"]

    response = None
    while response is None or response["status"] == "Running":
        time.sleep(1)  # Wait for query to complete
        response = client.get_query_results(queryId=query_id)

    results = response["results"]
    status = response["status"]

    return QueryResults(results=results, status=status)
