from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from observability_models import LogEvent, LogQuery, normalize_results


@dataclass
class ObservabilityConfig:
    log_group_name: str
    aws_region: str
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        log_group_name=os.environ.get("AWS_LOG_GROUP_NAME", "/aws/lambda/app"),
        aws_region=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )


def client_from_config(config: Optional[ObservabilityConfig] = None):
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {"region_name": cfg.aws_region}
    if cfg.aws_access_key_id and cfg.aws_secret_access_key:
        kwargs.update(
            aws_access_key_id=cfg.aws_access_key_id,
            aws_secret_access_key=cfg.aws_secret_access_key,
            aws_session_token=cfg.aws_session_token,
        )
    return boto3.client("logs", **kwargs)


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None):
        self.config = config or load_config()
        self.client = client_from_config(self.config)

    def write_log_event(self, event: LogEvent) -> Dict[str, Any]:
        payload = event.to_dict()
        stream_name = payload.get("service", "app")
        try:
            sequence_token = self._ensure_stream(stream_name)
            kwargs: Dict[str, Any] = {
                "logGroupName": self.config.log_group_name,
                "logStreamName": stream_name,
                "logEvents": [
                    {
                        "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
                        "message": __import__("json").dumps(payload, sort_keys=True),
                    }
                ],
            }
            if sequence_token:
                kwargs["sequenceToken"] = sequence_token
            return self.client.put_log_events(**kwargs)
        except (BotoCoreError, ClientError) as exc:
            return {"error": str(exc), "event": payload}

    def query_logs(self, query: LogQuery) -> List[Dict[str, Any]]:
        try:
            results = self.client.filter_log_events(
                logGroupName=self.config.log_group_name,
                startTime=self._to_ms(query.start_time),
                endTime=self._to_ms(query.end_time),
                filterPattern=self._build_filter_pattern(query),
                limit=query.limit,
            )
            events = []
            for item in results.get("events", []):
                message = item.get("message", "")
                try:
                    parsed = __import__("json").loads(message)
                except Exception:
                    parsed = {"message": message}
                parsed.setdefault("ingested_at", item.get("ingestionTime"))
                events.append(parsed)
            return normalize_results(events)
        except (BotoCoreError, ClientError):
            return []

    def _build_filter_pattern(self, query: LogQuery) -> str:
        parts = []
        if query.severity:
            parts.append(f'"severity":"{query.severity}"')
        for key, value in query.field_filters.items():
            parts.append(f'"{key}":"{value}"')
        return " ".join(parts)

    def _to_ms(self, value: str) -> int:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)

    def _ensure_stream(self, stream_name: str) -> Optional[str]:
        try:
            streams = self.client.describe_log_streams(
                logGroupName=self.config.log_group_name,
                logStreamNamePrefix=stream_name,
            ).get("logStreams", [])
            for stream in streams:
                if stream.get("logStreamName") == stream_name:
                    return stream.get("uploadSequenceToken")
            self.client.create_log_stream(logGroupName=self.config.log_group_name, logStreamName=stream_name)
            return None
        except (BotoCoreError, ClientError):
            return None
