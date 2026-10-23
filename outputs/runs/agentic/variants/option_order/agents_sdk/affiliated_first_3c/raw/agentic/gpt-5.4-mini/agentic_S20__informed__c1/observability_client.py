from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from observability_models import (
    LogIngestResponse,
    LogQueryResult,
    build_correlation_event,
    build_structured_event,
    normalize_log_event,
    normalize_severity,
    utc_now_iso,
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_LOG_GROUP = os.getenv("AWS_LOG_GROUP", "/application/managed-logs")
AWS_LOG_STREAM = os.getenv("AWS_LOG_STREAM", "integration-stream")


@dataclass
class CloudWatchLogClient:
    client: Any
    log_group: str = AWS_LOG_GROUP
    log_stream: str = AWS_LOG_STREAM

    @classmethod
    def from_env(cls) -> "CloudWatchLogClient":
        return cls(boto3.client("logs", region_name=AWS_REGION))

    def ensure_stream(self) -> None:
        try:
            self.client.create_log_group(logGroupName=self.log_group)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") != "ResourceAlreadyExistsException":
                raise

        try:
            self.client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") != "ResourceAlreadyExistsException":
                raise

    def write_event(self, event: Mapping[str, Any]) -> LogIngestResponse:
        normalized = normalize_log_event(event)
        self.ensure_stream()
        sequence_token = None
        try:
            streams = self.client.describe_log_streams(
                logGroupName=self.log_group,
                logStreamNamePrefix=self.log_stream,
                orderBy="LogStreamName",
                descending=False,
                limit=1,
            ).get("logStreams", [])
            if streams:
                sequence_token = streams[0].get("uploadSequenceToken")
        except Exception:
            sequence_token = None

        kwargs: Dict[str, Any] = {
            "logGroupName": self.log_group,
            "logStreamName": self.log_stream,
            "logEvents": [{"timestamp": int(datetime.now(timezone.utc).timestamp() * 1000), "message": str(normalized)}],
        }
        if sequence_token:
            kwargs["sequenceToken"] = sequence_token

        result = self.client.put_log_events(**kwargs)
        return LogIngestResponse(provider="Amazon CloudWatch Logs", status="ok", raw=result, request_id=result.get("nextSequenceToken"))

    def query(self, start_time: datetime, end_time: datetime, severity: Optional[str] = None, filters: Optional[Mapping[str, Any]] = None, limit: int = 50) -> LogQueryResult:
        self.ensure_stream()
        severity = normalize_severity(severity) if severity else None
        query_terms = []
        if severity:
            query_terms.append(f'severity = "{severity}"')
        for key, value in (filters or {}).items():
            query_terms.append(f'{key} = "{value}"')
        query_string = "fields @timestamp, @message | filter " + " and ".join(query_terms) if query_terms else "fields @timestamp, @message"

        response = self.client.start_query(
            logGroupName=self.log_group,
            startTime=int(start_time.replace(tzinfo=timezone.utc).timestamp()),
            endTime=int(end_time.replace(tzinfo=timezone.utc).timestamp()),
            queryString=query_string,
            limit=limit,
        )
        query_id = response.get("queryId")
        results = self.client.get_query_results(queryId=query_id)
        records: List[Dict[str, Any]] = []
        for row in results.get("results", []):
            rec = {item["field"].lstrip("@"): item.get("value") for item in row}
            records.append(rec)
        return LogQueryResult(provider="Amazon CloudWatch Logs", records=records, raw=results, next_token=query_id)


def get_client() -> CloudWatchLogClient:
    return CloudWatchLogClient.from_env()


def write_structured_log(message: str, severity: str = "INFO", **fields: Any) -> LogIngestResponse:
    return get_client().write_event(build_structured_event(message, severity=severity, **fields))


def write_correlated_logs(messages: Iterable[str], correlation_id: str, severity: str = "INFO", **fields: Any) -> List[LogIngestResponse]:
    client = get_client()
    responses: List[LogIngestResponse] = []
    for message in messages:
        responses.append(client.write_event(build_correlation_event(message, correlation_id, severity=severity, **fields)))
    return responses


def query_recent_logs(hours: int = 1, severity: Optional[str] = None, **field_filters: Any) -> LogQueryResult:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    return get_client().query(start, end, severity=severity, filters=field_filters)
