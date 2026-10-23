"""
Summarize federated-login audit events using AWS CloudWatch Logs Insights.
Queries Auth0 log events forwarded to CloudWatch and produces login analytics.
"""

import os
import json
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

import boto3
from botocore.exceptions import ClientError

from identity_models import AuditSummary


CLOUDWATCH_LOG_GROUP = os.getenv("AUTH0_CLOUDWATCH_LOG_GROUP", "/auth0/logs")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def _build_insights_query(
    start_time: datetime,
    end_time: datetime,
    filters: Optional[Dict[str, str]] = None,
) -> str:
    """Build a CloudWatch Logs Insights query for Auth0 login events."""
    base_query = f"""
fields @timestamp, @message
| filter @logStream like /auth0/
| filter @timestamp >= "{start_time.isoformat()}"
| filter @timestamp <= "{end_time.isoformat()}"
| filter type in ["s", "f", "scp", "fs"]
"""
    if filters:
        for key, value in filters.items():
            base_query += f'| filter data."{key}" = "{value}"\n'

    base_query += """
| stats
    count(*) as total_events,
    sum(type="s") as successful,
    sum(type="f") as failed,
    count_distinct(data.user_id) as unique_users
"""
    return base_query


def _build_provider_breakdown_query(
    start_time: datetime,
    end_time: datetime,
) -> str:
    """Build a query to break down events by identity provider."""
    return f"""
fields @timestamp, @message
| filter @logStream like /auth0/
| filter @timestamp >= "{start_time.isoformat()}"
| filter @timestamp <= "{end_time.isoformat()}"
| filter type = "s"
| parse @message /"connection":"(?<connection>[^"]+)"/
| stats count(*) as event_count by connection
"""


def _build_hourly_query(
    start_time: datetime,
    end_time: datetime,
) -> str:
    """Build a query for hourly event distribution."""
    return f"""
fields @timestamp
| filter @logStream like /auth0/
| filter @timestamp >= "{start_time.isoformat()}"
| filter @timestamp <= "{end_time.isoformat()}"
| stats count(*) as events by bin(1h)
"""


async def summarize_audit_events(
    hours: int = 24,
    log_group: Optional[str] = None,
    region: Optional[str] = None,
    filters: Optional[Dict[str, str]] = None,
) -> AuditSummary:
    """
    Summarize federated-login audit events from CloudWatch Logs Insights.

    Queries Auth0 log streams forwarded to AWS CloudWatch and aggregates
    login statistics including success/failure rates, unique users, and
    provider breakdown.
    """
    log_group_name = log_group or CLOUDWATCH_LOG_GROUP
    aws_region = region or AWS_REGION

    client = boto3.client("logs", region_name=aws_region)

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    query = _build_insights_query(start_time, end_time, filters)

    try:
        start_response = client.start_query(
            logGroupName=log_group_name,
            startTime=int(start_time.timestamp()),
            endTime=int(end_time.timestamp()),
            queryString=query,
        )
        query_id = start_response["queryId"]

        summary = await _poll_query_results(client, query_id)
        providers = await _fetch_provider_breakdown(client, log_group_name, start_time, end_time)
        hourly = await _fetch_hourly_distribution(client, log_group_name, start_time, end_time)

        summary.providers = providers
        summary.events_by_hour = hourly

        return summary

    except ClientError as exc:
        raise RuntimeError(f"CloudWatch Logs Insights query failed: {exc}") from exc


async def _poll_query_results(
    client,
    query_id: str,
    max_attempts: int = 30,
    poll_interval: int = 2,
) -> AuditSummary:
    """Poll CloudWatch for query completion and return results."""
    import asyncio as aio

    for _ in range(max_attempts):
        response = client.get_query_results(queryId=query_id)
        status = response["status"]

        if status == "Complete":
            return _parse_summary_results(response["results"])
        elif status in ("Failed", "Cancelled"):
            raise RuntimeError(f"CloudWatch query {status}")

        await aio.sleep(poll_interval)

    raise RuntimeError("CloudWatch query timed out")


def _parse_summary_results(results: List[List[Dict[str, str]]]) -> AuditSummary:
    """Parse CloudWatch Insights results into an AuditSummary."""
    summary = AuditSummary()

    if not results:
        return summary

    for row in results:
        for field in row:
            name = field.get("field", "")
            value = field.get("value", "0")

            if name == "total_events":
                summary.total_events = int(value)
            elif name == "successful":
                summary.successful_logins = int(value)
            elif name == "failed":
                summary.failed_logins = int(value)
            elif name == "unique_users":
                summary.unique_users = int(value)

    return summary


async def _fetch_provider_breakdown(
    client,
    log_group: str,
    start_time: datetime,
    end_time: datetime,
) -> Dict[str, int]:
    """Fetch event counts broken down by identity provider."""
    import asyncio as aio

    query = _build_provider_breakdown_query(start_time, end_time)
    start_response = client.start_query(
        logGroupName=log_group,
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
        queryString=query,
    )

    for _ in range(30):
        response = client.get_query_results(queryId=start_response["queryId"])
        if response["status"] == "Complete":
            providers = {}
            for row in response["results"]:
                connection = "unknown"
                count = 0
                for field in row:
                    if field["field"] == "connection":
                        connection = field["value"]
                    elif field["field"] == "event_count":
                        count = int(field["value"])
                providers[connection] = count
            return providers
        await aio.sleep(2)

    return {}


async def _fetch_hourly_distribution(
    client,
    log_group: str,
    start_time: datetime,
    end_time: datetime,
) -> Dict[str, int]:
    """Fetch hourly event distribution."""
    import asyncio as aio

    query = _build_hourly_query(start_time, end_time)
    start_response = client.start_query(
        logGroupName=log_group,
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
        queryString=query,
    )

    for _ in range(30):
        response = client.get_query_results(queryId=start_response["queryId"])
        if response["status"] == "Complete":
            hourly = {}
            for row in response["results"]:
                timestamp = ""
                count = 0
                for field in row:
                    if field["field"] == "bin(1h)":
                        timestamp = field["value"]
                    elif field["field"] == "events":
                        count = int(field["value"])
                hourly[timestamp] = count
            return hourly
        await aio.sleep(2)

    return {}


def format_summary_response(summary: AuditSummary) -> Dict[str, Any]:
    """Format the audit summary for API response."""
    return {
        "total_events": summary.total_events,
        "successful_logins": summary.successful_logins,
        "failed_logins": summary.failed_logins,
        "unique_users": summary.unique_users,
        "success_rate": (
            summary.successful_logins / summary.total_events
            if summary.total_events > 0
            else 0
        ),
        "providers": summary.providers,
        "events_by_hour": summary.events_by_hour,
        "source": "aws_cloudwatch_logs_insights",
        "log_group": CLOUDWATCH_LOG_GROUP,
    }


if __name__ == "__main__":
    async def main():
        summary = await summarize_audit_events(hours=24)
        print(json.dumps(format_summary_response(summary), indent=2))

    asyncio.run(main())
