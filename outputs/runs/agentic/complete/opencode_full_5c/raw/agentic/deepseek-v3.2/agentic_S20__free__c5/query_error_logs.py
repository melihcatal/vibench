import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_logging_client
from observability_models import LogQuery, LogEntry


def query_error_logs(
    service_name: str, hours_back: int = 24, severity: str = "ERROR", limit: int = 100
) -> List[LogEntry]:
    """
    Query recent error log entries from AWS CloudWatch Logs filtered by severity and time range.

    Args:
        service_name: Name of the service to query logs for
        hours_back: Number of hours to look back (default: 24)
        severity: Minimum severity level to filter (ERROR, CRITICAL, WARNING)
        limit: Maximum number of log entries to return

    Returns:
        List of LogEntry objects containing error log data
    """
    try:
        import boto3
        from botocore.config import Config

        client = boto3.client(
            "logs",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            config=Config(retries={"max_attempts": 3}),
        )

        log_group_name = f"/aws/lambda/{service_name}"
        if service_name.startswith("ecs/"):
            log_group_name = f"/ecs/{service_name}"
        elif service_name.startswith("eks/"):
            log_group_name = f"/aws/eks/{service_name}"

        end_time = int(datetime.utcnow().timestamp() * 1000)
        start_time = int(
            (datetime.utcnow() - timedelta(hours=hours_back)).timestamp() * 1000
        )

        severity_filter = ""
        if severity == "ERROR":
            severity_filter = "?ERROR ?Exception ?Failed ?Failure"
        elif severity == "CRITICAL":
            severity_filter = "?CRITICAL ?Fatal ?panic"
        elif severity == "WARNING":
            severity_filter = "?WARNING ?Warning ?Caution"

        query_string = f"""
        fields @timestamp, @message, @logStream, @log
        | filter @message like /{severity_filter}/
        | sort @timestamp desc
        | limit {limit}
        """

        response = client.start_query(
            logGroupName=log_group_name,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=limit,
        )

        query_id = response["queryId"]

        import time

        status = "Running"
        while status == "Running":
            time.sleep(1)
            result = client.get_query_results(queryId=query_id)
            status = result["status"]

        log_entries = []
        if status == "Complete" and "results" in result:
            for row in result["results"]:
                entry_data = {}
                for field in row:
                    entry_data[field["field"]] = field["value"]

                log_entry = LogEntry(
                    timestamp=entry_data.get("@timestamp", ""),
                    message=entry_data.get("@message", ""),
                    service=service_name,
                    level=severity,
                    log_stream=entry_data.get("@logStream", ""),
                    log_group=entry_data.get("@log", ""),
                    raw_data=entry_data,
                )
                log_entries.append(log_entry)

        print(
            f"Queried {len(log_entries)} error logs from AWS CloudWatch for service: {service_name}"
        )
        return log_entries

    except Exception as e:
        print(f"Failed to query error logs from AWS CloudWatch: {e}")
        return []
