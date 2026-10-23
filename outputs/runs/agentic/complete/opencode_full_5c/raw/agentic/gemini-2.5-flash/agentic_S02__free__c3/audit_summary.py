import os
import boto3
from datetime import datetime, timedelta
from typing import Dict, Any, List


def summarize_cloudwatch_login_events(
    log_group_name: str,
    start_time: datetime,
    end_time: datetime,
    region_name: str = "us-east-1",
) -> Dict[str, Any]:
    """
    Summarizes federated login audit events from AWS CloudWatch Logs.
    This function searches for specific log patterns and counts occurrences.
    """
    client = boto3.client("logs", region_name=region_name)

    # Example: search for successful logins and failed logins
    # In a real scenario, you'd define specific log patterns for your audit events
    queries = [
        "fields @timestamp, @message | filter @message like /LoginSuccess/ | stats count() as successful_logins by bin(1h)",
        "fields @timestamp, @message | filter @message like /LoginFailure/ | stats count() as failed_logins by bin(1h)",
    ]

    summary = {
        "log_group_name": log_group_name,
        "start_time": str(start_time),
        "end_time": str(end_time),
        "results": [],
    }

    for query_string in queries:
        start_query_response = client.start_query(
            logGroupName=log_group_name,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000),
            queryString=query_string,
            limit=100,
        )

        query_id = start_query_response["queryId"]

        response = None
        while (
            response is None
            or response["status"] == "Running"
            or response["status"] == "Scheduled"
        ):
            print(f"Waiting for query {query_id} to complete...")
            # In a real app, you'd implement a proper backoff strategy
            import time

            time.sleep(1)
            response = client.get_query_results(queryId=query_id)

        query_results = {"query": query_string, "data": []}
        for row in response["results"]:
            row_data = {
                field["field"]: field["value"]
                for field in row
                if field["field"] != "@ptr"
            }
            query_results["data"].append(row_data)
        summary["results"].append(query_results)

    return summary


if __name__ == "__main__":
    # Set AWS credentials as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    # or configure boto3 in other ways.
    # Example: export AWS_REGION='us-east-1'
    # Example: export CLOUDWATCH_LOG_GROUP_NAME='/aws/lambda/your-login-auditor'

    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    CLOUDWATCH_LOG_GROUP_NAME = os.environ.get(
        "CLOUDWATCH_LOG_GROUP_NAME", "/aws/vendedlogs/log-group-for-login-audits"
    )

    if not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get(
        "AWS_SECRET_ACCESS_KEY"
    ):
        print(
            "WARNING: AWS credentials not found in environment variables. This script may fail."
        )

    end_t = datetime.now()
    start_t = end_t - timedelta(hours=24)  # Last 24 hours

    print(
        f"Summarizing login events in log group '{CLOUDWATCH_LOG_GROUP_NAME}' from {start_t} to {end_t}..."
    )
    try:
        audit_summary = summarize_cloudwatch_login_events(
            log_group_name=CLOUDWATCH_LOG_GROUP_NAME,
            start_time=start_t,
            end_time=end_t,
            region_name=AWS_REGION,
        )
        print("\nAudit Summary:")
        print(json.dumps(audit_summary, indent=2))
    except Exception as e:
        print(f"Error summarizing CloudWatch Logs: {e}")
