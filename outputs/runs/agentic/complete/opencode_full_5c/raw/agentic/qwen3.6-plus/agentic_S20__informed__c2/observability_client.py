import os
import time
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from aliyun.log import LogClient, PutLogsRequest, LogItem, GetLogsRequest
from aliyun.log.logresponse import LogResponse
from aliyun.log.putlogsrequest import PutLogsRequest as SlsPutLogsRequest
from aliyun.log.getlogsrequest import GetLogsRequest as SlsGetLogsRequest
from aliyun.log.listlogstoresrequest import ListLogstoresRequest

from observability_models import (
    StructuredLogEvent,
    LogQueryResult,
    SlsClientConfig,
    LogSeverity,
)

logger = logging.getLogger(__name__)


class ObservabilityClient:
    def __init__(self, config: Optional[SlsClientConfig] = None):
        self.config = config or SlsClientConfig.from_env()
        self._client = LogClient(
            self.config.endpoint,
            self.config.access_key_id,
            self.config.access_key_secret,
        )

    def put_logs(
        self, logs: list[StructuredLogEvent], topic: str = "", source: str = ""
    ) -> dict:
        log_items = []
        for log_event in logs:
            content = log_event.to_sls_log_content()
            log_item = LogItem()
            log_item.set_time(
                int(datetime.fromisoformat(log_event.timestamp).timestamp())
            )
            log_item.set_contents(content)
            log_items.append(log_item)

        request = PutLogsRequest(
            project=self.config.project,
            logstore=self.config.logstore,
            topic=topic,
            source=source,
            logitems=log_items,
        )
        response = self._client.put_logs(request)
        return {
            "request_id": response.get_request_id(),
            "status": response.get_status(),
            "log_count": len(logs),
        }

    def get_logs(
        self,
        query: str = "*",
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        topic: str = "",
        line: int = 100,
        offset: int = 0,
        reverse: bool = True,
    ) -> LogQueryResult:
        if from_time is None:
            from_time = datetime.now(timezone.utc) - timedelta(hours=1)
        if to_time is None:
            to_time = datetime.now(timezone.utc)

        from_ts = int(from_time.timestamp())
        to_ts = int(to_time.timestamp())

        request = GetLogsRequest(
            project=self.config.project,
            logstore=self.config.logstore,
            fromTime=from_ts,
            toTime=to_ts,
            topic=topic,
            query=query,
            line=line,
            offset=offset,
            reverse=reverse,
        )
        response = self._client.get_logs(request)
        logs_data = response.get_logs()
        parsed_logs = []
        for log_entry in logs_data:
            parsed_log = {}
            for key in log_entry:
                parsed_log[key] = log_entry[key]
            parsed_logs.append(parsed_log)

        return LogQueryResult(
            logs=parsed_logs,
            count=response.get_count(),
            query_id=response.get_request_id(),
            completed=True,
            progress=1.0,
        )

    def get_log_count(
        self,
        query: str = "*",
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        topic: str = "",
    ) -> int:
        if from_time is None:
            from_time = datetime.now(timezone.utc) - timedelta(hours=1)
        if to_time is None:
            to_time = datetime.now(timezone.utc)

        from_ts = int(from_time.timestamp())
        to_ts = int(to_time.timestamp())

        request = GetLogsRequest(
            project=self.config.project,
            logstore=self.config.logstore,
            fromTime=from_ts,
            toTime=to_ts,
            topic=topic,
            query=query,
            line=0,
            offset=0,
            reverse=False,
        )
        response = self._client.get_logs(request)
        return response.get_count()

    def list_logstores(self) -> list[str]:
        request = ListLogstoresRequest(project=self.config.project)
        response = self._client.list_logstores(request)
        return response.get_logstores()


def build_error_query(
    severity: str = "ERROR",
    from_time: Optional[datetime] = None,
    to_time: Optional[datetime] = None,
) -> str:
    severity_upper = severity.upper()
    return f"severity: {severity_upper}"


def build_field_filter_query(field_name: str, field_value: str) -> str:
    return f"{field_name}: {field_value}"


def build_time_range_query(
    base_query: str = "*",
    from_time: Optional[datetime] = None,
    to_time: Optional[datetime] = None,
) -> tuple[datetime, datetime]:
    if from_time is None:
        from_time = datetime.now(timezone.utc) - timedelta(hours=1)
    if to_time is None:
        to_time = datetime.now(timezone.utc)
    return from_time, to_time


def normalize_log_for_display(log_entry: dict) -> dict:
    normalized = {}
    for key, value in log_entry.items():
        normalized_key = key.replace("__", ".")
        normalized[normalized_key] = value
    return normalized


def extract_error_messages(query_result: LogQueryResult) -> list[dict]:
    error_logs = query_result.filter_by_severity(LogSeverity.ERROR.value)
    fatal_logs = query_result.filter_by_severity(LogSeverity.FATAL.value)
    return error_logs + fatal_logs


def group_logs_by_correlation_id(logs: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for log in logs:
        corr_id = log.get("correlation_id", "unknown")
        if corr_id not in grouped:
            grouped[corr_id] = []
        grouped[corr_id].append(log)
    return grouped
