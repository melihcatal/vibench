import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError

from observability_client import client
from observability_models import LogEvent, LogLevel, LogQuery, LogQueryResult


def fetch_recent_logs(
    field_filters: Dict[str, str] = None, hours: int = 1, limit: int = 100
) -> LogQueryResult:
    """
    Retrieve recent log results from AWS CloudWatch Logs Insights filtered by field values.

    Args:
        field_filters: Dictionary of field=value filters
        hours: Hours to look back
        limit: Maximum number of results

    Returns:
        LogQueryResult with filtered logs
    """
    try:
        if field_filters is None:
            field_filters = {}

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        filter_parts = []
        for field, value in field_filters.items():
            if field.startswith("@"):
                field_name = field
            else:
                field_name = field

            filter_parts.append(f"{field_name} = '{value}'")

        if filter_parts:
            filter_str = " and ".join(filter_parts)
            query_string = f"""
            fields @timestamp, @message, level, correlation_id, service, environment
            | filter {filter_str}
            | sort @timestamp desc
            | limit {limit}
            """
        else:
            query_string = f"""
            fields @timestamp, @message, level, correlation_id, service, environment
            | sort @timestamp desc
            | limit {limit}
            """

        print(f"Querying AWS CloudWatch Logs Insights with filters...")
        print(f"Time range: {start_time} to {end_time}")
        print(f"Field filters: {field_filters}")
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

            if "message" in log_data:
                try:
                    log_event = LogEvent(
                        message=log_data.get("message", ""),
                        level=log_data.get("level", LogLevel.INFO),
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
        print(f"Query completed. Found {len(logs)} logs matching filters.")
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
        print(f"Unexpected error fetching logs: {e}")

        return LogQueryResult(
            query_id="error", status="Failed", results=[], statistics={"error": str(e)}
        )


def fetch_logs_by_correlation_id(
    correlation_id: str, hours: int = 24
) -> LogQueryResult:
    """
    Fetch all logs for a specific correlation ID.

    Args:
        correlation_id: The correlation ID to search for
        hours: Hours to look back

    Returns:
        LogQueryResult with correlated logs
    """
    return fetch_recent_logs(
        field_filters={"correlation_id": correlation_id}, hours=hours, limit=500
    )


def fetch_logs_by_service(
    service_name: str, hours: int = 1, level: Optional[str] = None
) -> LogQueryResult:
    """
    Fetch logs for a specific service.

    Args:
        service_name: Service name to filter by
        hours: Hours to look back
        level: Optional log level filter

    Returns:
        LogQueryResult with service logs
    """
    field_filters = {"service": service_name}
    if level:
        field_filters["level"] = level

    return fetch_recent_logs(field_filters=field_filters, hours=hours, limit=200)


def get_log_statistics(hours: int = 1) -> Dict[str, Any]:
    """
    Get statistics about recent logs.

    Args:
        hours: Hours to look back

    Returns:
        Dictionary with log statistics
    """
    query_string = """
    stats count(*) as total_logs, count_distinct(service) as unique_services, 
           count(filter level in ["ERROR", "CRITICAL"]) as error_count,
           count_distinct(correlation_id) as unique_correlation_ids
    | sort @timestamp desc
    """

    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        response = client.cloudwatch_logs_client.start_query(
            logGroupName=client._log_group_name,
            startTime=int(start_time.timestamp()),
            endTime=int(end_time.timestamp()),
            queryString=query_string,
            limit=1,
        )

        query_id = response["queryId"]

        for _ in range(30):
            time.sleep(1)
            response = client.cloudwatch_logs_client.get_query_results(queryId=query_id)
            if response["status"] in ["Complete", "Failed", "Cancelled"]:
                break

        if response["status"] == "Complete" and response.get("results"):
            stats = {}
            for field in response["results"][0]:
                stats[field.get("field")] = field.get("value")

            return {
                "time_range_hours": hours,
                "query_id": query_id,
                "statistics": stats,
            }

        return {
            "time_range_hours": hours,
            "query_id": query_id,
            "statistics": {},
            "status": response["status"],
        }

    except Exception as e:
        print(f"Error getting log statistics: {e}")
        return {"time_range_hours": hours, "error": str(e)}
