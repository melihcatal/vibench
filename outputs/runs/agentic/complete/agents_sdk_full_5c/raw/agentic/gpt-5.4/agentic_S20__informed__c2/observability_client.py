from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Iterable, List, Optional

import boto3

from observability_models import LogEvent, LogQueryResult, normalize_cloudwatch_result


class CloudWatchObservabilityClient:
    def __init__(
        self,
        log_group_name: Optional[str] = None,
        log_stream_name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> None:
        self.region_name = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.log_group_name = log_group_name or os.getenv("CLOUDWATCH_LOG_GROUP_NAME")
        self.log_stream_name = log_stream_name or os.getenv("CLOUDWATCH_LOG_STREAM_NAME", "application")
        if not self.log_group_name:
            raise ValueError("CLOUDWATCH_LOG_GROUP_NAME is required")
        self.logs_client = boto3.client("logs", region_name=self.region_name)

    def ensure_log_stream(self) -> None:
        try:
            self.logs_client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
            )
        except self.logs_client.exceptions.ResourceAlreadyExistsException:
            return

    def _get_sequence_token(self) -> Optional[str]:
        response = self.logs_client.describe_log_streams(
            logGroupName=self.log_group_name,
            logStreamNamePrefix=self.log_stream_name,
        )
        for stream in response.get("logStreams", []):
            if stream.get("logStreamName") == self.log_stream_name:
                return stream.get("uploadSequenceToken")
        return None

    def put_structured_logs(self, events: Iterable[LogEvent]) -> dict:
        self.ensure_log_stream()
        log_events = []
        for event in events:
            payload = event.to_structured_payload()
            log_events.append(
                {
                    "timestamp": int(datetime.fromisoformat(event.timestamp).timestamp() * 1000),
                    "message": json.dumps(payload, separators=(",", ":")),
                }
            )
        log_events.sort(key=lambda x: x["timestamp"])
        request = {
            "logGroupName": self.log_group_name,
            "logStreamName": self.log_stream_name,
            "logEvents": log_events,
        }
        sequence_token = self._get_sequence_token()
        if sequence_token:
            request["sequenceToken"] = sequence_token
        return self.logs_client.put_log_events(**request)

    def start_query(self, query_string: str, minutes: int = 15) -> str:
        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=minutes)
        response = self.logs_client.start_query(
            logGroupName=self.log_group_name,
            startTime=int(start.timestamp()),
            endTime=int(end.timestamp()),
            queryString=query_string,
        )
        return response["queryId"]

    def wait_for_query_results(self, query_id: str, timeout_seconds: int = 30) -> List[LogQueryResult]:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            response = self.logs_client.get_query_results(queryId=query_id)
            status = response.get("status")
            if status == "Complete":
                return [normalize_cloudwatch_result(item) for item in response.get("results", [])]
            if status in {"Failed", "Cancelled", "Timeout", "Unknown"}:
                raise RuntimeError(f"CloudWatch Logs Insights query failed with status={status}")
            time.sleep(1)
        raise TimeoutError("Timed out waiting for CloudWatch Logs Insights results")
