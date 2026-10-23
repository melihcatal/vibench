import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import boto3
from botocore.config import Config


class ObservabilityClient:
    def __init__(self):
        self._cloudwatch_client = None
        self._cloudwatch_logs_client = None
        self._log_group_name = os.getenv("AWS_CLOUDWATCH_LOG_GROUP", "application-logs")
        self._log_stream_prefix = os.getenv("AWS_CLOUDWATCH_LOG_STREAM_PREFIX", "app")

    @property
    def cloudwatch_client(self):
        if self._cloudwatch_client is None:
            self._cloudwatch_client = boto3.client(
                "cloudwatch",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                config=Config(retries={"max_attempts": 3}),
            )
        return self._cloudwatch_client

    @property
    def cloudwatch_logs_client(self):
        if self._cloudwatch_logs_client is None:
            self._cloudwatch_logs_client = boto3.client(
                "logs",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                config=Config(retries={"max_attempts": 3}),
            )
        return self._cloudwatch_logs_client

    def get_log_stream_name(self, component: str = "default") -> str:
        timestamp = datetime.utcnow().strftime("%Y/%m/%d")
        return f"{self._log_stream_prefix}/{component}/{timestamp}"

    def create_log_event(
        self,
        message: str,
        level: str = "INFO",
        extra_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        event = {
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
            "message": message,
            "level": level,
            "service": os.getenv("SERVICE_NAME", "unknown-service"),
            "environment": os.getenv("ENVIRONMENT", "development"),
        }

        if extra_fields:
            event.update(extra_fields)

        return event

    def parse_log_query_response(
        self, response: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        logs = []
        for result in response.get("results", []):
            log_entry = {}
            for field in result:
                if field.get("field") == "@timestamp":
                    log_entry["timestamp"] = field.get("value")
                elif field.get("field") == "@message":
                    log_entry["message"] = field.get("value")
                elif field.get("field") == "level":
                    log_entry["level"] = field.get("value")
                elif field.get("field") == "correlation_id":
                    log_entry["correlation_id"] = field.get("value")
                else:
                    log_entry[field.get("field", "unknown")] = field.get("value")
            logs.append(log_entry)
        return logs

    def build_time_range_filter(self, hours: int = 1) -> Dict[str, int]:
        end_time = int(datetime.utcnow().timestamp() * 1000)
        start_time = int(
            (datetime.utcnow() - timedelta(hours=hours)).timestamp() * 1000
        )
        return {"startTime": start_time, "endTime": end_time}


client = ObservabilityClient()
