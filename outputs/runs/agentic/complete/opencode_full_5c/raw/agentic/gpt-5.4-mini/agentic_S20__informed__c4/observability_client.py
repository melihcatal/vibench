from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3

from observability_models import LogQuery, LogResult, build_log_event, normalize_iso8601

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_LOG_GROUP = os.getenv('AWS_LOG_GROUP', '/managed/observability')
AWS_LOG_STREAM = os.getenv('AWS_LOG_STREAM', 'app')


@dataclass
class CloudWatchLogClient:
    client: Any
    log_group: str
    log_stream: str

    def ensure_stream(self) -> None:
        try:
            self.client.create_log_group(logGroupName=self.log_group)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        try:
            self.client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def put_event(self, event: dict[str, Any]) -> dict[str, Any]:
        self.ensure_stream()
        timestamp = int(datetime.fromisoformat(normalize_iso8601(event.get('timestamp'))).timestamp() * 1000)
        return self.client.put_log_events(logGroupName=self.log_group, logStreamName=self.log_stream, logEvents=[{'timestamp': timestamp, 'message': event['message'] if isinstance(event.get('message'), str) else str(event)}])

    def query(self, query: LogQuery) -> LogResult:
        start_ms = int(datetime.fromisoformat(query.start_time).timestamp() * 1000)
        end_ms = int(datetime.fromisoformat(query.end_time).timestamp() * 1000)
        streams = self.client.describe_log_streams(logGroupName=self.log_group, orderBy='LastEventTime', descending=True).get('logStreams', [])
        records: list[dict[str, Any]] = []
        for stream in streams[:10]:
            events = self.client.get_log_events(logGroupName=self.log_group, logStreamName=stream['logStreamName'], startTime=start_ms, endTime=end_ms, startFromHead=True).get('events', [])
            for item in events:
                message = item.get('message', '')
                if query.severity and query.severity.upper() not in message.upper():
                    continue
                if all(str(v) in message for v in query.filters.values()):
                    records.append({'timestamp': item.get('timestamp'), 'message': message, 'stream': stream['logStreamName']})
        return LogResult(records=records)


def get_client() -> CloudWatchLogClient:
    return CloudWatchLogClient(boto3.client('logs', region_name=AWS_REGION), AWS_LOG_GROUP, AWS_LOG_STREAM)


def recent_time_window(minutes: int = 60) -> tuple[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return start.isoformat(), end.isoformat()


def write_structured(message: str, **fields: Any) -> dict[str, Any]:
    return get_client().put_event(build_log_event(message, **fields))


def fetch_recent(severity: str | None = None, filters: dict[str, Any] | None = None, minutes: int = 60) -> LogResult:
    start, end = recent_time_window(minutes)
    return get_client().query(LogQuery(start_time=start, end_time=end, severity=severity, filters=filters or {}))
