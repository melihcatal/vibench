import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError

from observability_client import client
from observability_models import LogEvent, LogLevel, LogQuery, LogQueryResult


def query_error_logs(hours: int = 1, limit: int = 100) -> LogQueryResult:
    """
    Query recent error log entries from AWS CloudWatch Logs Insights.

    Args:
        hours: Hours to look back
        limit: Maximum number of results

    Returns:
        LogQueryResult with error logs
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        query_string = """
        fields @timestamp, @message, level, correlation_id, service, environment
        | filter level in ["ERROR", "CRITICAL", "FATAL"]
        | sort @timestamp desc
        | limit {}
        """.format(limit)

        print(f"Querying AWS CloudWatch Logs Insights for error logs...")
        print(f"Time range: {start_time} to {end_time}")
        print(f"Query: {query_string.strip()}")

        response = client.cloudwatch_logs_client.start_query(
            logGroupName=client._log_group_name,
            startTime=int(start_time.timestamp()),
            endTime=int(end_time.timestamp()),
            queryString=query_string,
            limit=limit,
        )

        query_id = response["queryId"]
        print(f"Started CloudWatch Logs Insights query: {query_id}")

        query_status = None
        query_results = None

        for _ in range(30):
            time.sleep(1)

            response = client.cloudwatch_logs_client.get_query_results(queryId=query_id)

            query_status = response["status"]
            print(f"Query status: {query_status}")

            if query_status in ["Complete", "Failed", "Cancelled"]:
                query_results = response
                break

        if query_status != "Complete":
            print(f"Query did not complete successfully. Status: {query_status}")
            return LogQueryResult(
                query_id=query_id,
                status=query_status,
                results=[],
                statistics=query_results.get("statistics") if query_results else None,
            )

        logs = []
        for result in query_results.get("results", []):
            log_data = {}
            for field in result:
                field_name = field.get("field", "").lstrip("@")
                field_value = field.get("value", "")

                if field_name == "timestamp":
                    try:
                        field_value = datetime.fromisoformat(
                            field_value.replace("Z", "+00:00")
                        )
                    except:
                        pass
                elif field_name == "level":
                    try:
                        field_value = LogLevel(field_value)
                    except:
                        field_value = LogLevel.INFO

                log_data[field_name] = field_value

            if "message" in log_data and "timestamp" in log_data:
                try:
                    log_event = LogEvent(
                        message=log_data.get("message", ""),
                        level=log_data.get("level", LogLevel.ERROR),
                        timestamp=log_data.get("timestamp"),
                        correlation_id=log_data.get("correlation_id"),
                        service=log_data.get("service"),
                        environment=log_data.get("environment"),
                        extra_fields={
                            k: v
                            for k, v in log_data.items()
                            if k
                            not in [
                                "message",
                                "level",
                                "timestamp",
                                "correlation_id",
                                "service",
                                "environment",
                            ]
                        },
                    )
                    logs.append(log_event)
                except Exception as e:
                    print(f"Error parsing log event: {e}")

        statistics = query_results.get("statistics", {})
        print(f"Query completed. Found {len(logs)} error logs.")
        print(f"Statistics: {statistics}")

        return LogQueryResult(
            query_id=query_id, status=query_status, results=logs, statistics=statistics
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        print(f"AWS CloudWatch Logs Insights query failed: {error_code} - {error_msg}")

        return LogQueryResult(
            query_id="error",
            status="Failed",
            results=[],
            statistics={"error": error_msg, "error_code": error_code},
        )

    except Exception as e:
        print(f"Unexpected error querying logs: {e}")

        return LogQueryResult(
            query_id="error", status="Failed", results=[], statistics={"error": str(e)}
        )


def get_error_summary(hours: int = 1) -> Dict[str, Any]:
    """
    Get summary statistics for error logs.

    Args:
        hours: Hours to look back

    Returns:
        Dictionary with error summary
    """
    result = query_error_logs(hours=hours)

    if not result.results:
        return {
            "total_errors": 0,
            "services_affected": [],
            "time_range_hours": hours,
            "query_status": result.status,
        }

    services = set()
    error_messages = {}

    for log in result.results:
        if log.service:
            services.add(log.service)

        msg_key = log.message[:100]
        error_messages[msg_key] = error_messages.get(msg_key, 0) + 1

    sorted_errors = sorted(error_messages.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_errors": len(result.results),
        "services_affected": list(services),
        "most_common_errors": sorted_errors[:5],
        "time_range_hours": hours,
        "query_id": result.query_id,
        "query_status": result.status,
        "earliest_error": min(
            [log.timestamp for log in result.results if log.timestamp]
        ).isoformat()
        if result.results
        else None,
        "latest_error": max(
            [log.timestamp for log in result.results if log.timestamp]
        ).isoformat()
        if result.results
        else None,
    }
