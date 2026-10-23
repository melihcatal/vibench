import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from google.cloud import logging_v2
from google.cloud.logging_v2.types import LogEntry as GcpLogEntry
from google.protobuf.timestamp_pb2 import Timestamp

from observability_models import LogEntry, LogQueryResult


class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError(
                "Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
            )
        self.logging_client = logging_v2.LoggerClient()

    def _to_gcp_log_entry(self, log_entry_data: LogEntry) -> GcpLogEntry:
        gcp_log_entry = GcpLogEntry(
            severity=log_entry_data.severity.upper(),
            resource={
                "type": log_entry_data.resource_type,
                "labels": log_entry_data.resource_labels,
            },
            labels=log_entry_data.labels,
        )

        if log_entry_data.message:
            gcp_log_entry.text_payload = log_entry_data.message

        if log_entry_data.json_payload:
            gcp_log_entry.json_payload.update(log_entry_data.json_payload)

        if log_entry_data.timestamp:
            dt_object = datetime.fromisoformat(
                log_entry_data.timestamp.replace("Z", "+00:00")
            )
            gcp_log_entry.timestamp.FromDatetime(dt_object)

        if log_entry_data.trace:
            gcp_log_entry.trace = log_entry_data.trace
        if log_entry_data.span_id:
            gcp_log_entry.span_id = log_entry_data.span_id
        if log_entry_data.insert_id:
            gcp_log_entry.insert_id = log_entry_entry.insert_id

        return gcp_log_entry

    def write_log_entry(self, log_name: str, log_entry_data: LogEntry):
        logger_name = f"projects/{self.project_id}/logs/{log_name}"
        entries = [self._to_gcp_log_entry(log_entry_data)]
        self.logging_client.write_log_entries(entries=entries, log_name=logger_name)

    def write_log_entries(self, log_name: str, log_entry_datas: List[LogEntry]):
        logger_name = f"projects/{self.project_id}/logs/{log_name}"
        entries = [self._to_gcp_log_entry(data) for data in log_entry_datas]
        self.logging_client.write_log_entries(entries=entries, log_name=logger_name)

    def query_logs(
        self,
        filter_str: str,
        order_by: str = "timestamp desc",
        page_size: int = 100,
        max_entries: int = 1000,
    ) -> List[LogQueryResult]:
        project_name = f"projects/{self.project_id}"
        query_results: List[LogQueryResult] = []
        for entry in self.logging_client.list_log_entries(
            resource_names=[project_name],
            filter=filter_str,
            order_by=order_by,
            page_size=page_size,
        ):
            if len(query_results) >= max_entries:
                break

            message = (
                entry.text_payload
                if entry.text_payload
                else (
                    json.dumps(dict(entry.json_payload)) if entry.json_payload else ""
                )
            )

            query_results.append(
                LogQueryResult(
                    timestamp=entry.timestamp.isoformat(),
                    severity=entry.severity.name,
                    message=message,
                    json_payload=dict(entry.json_payload)
                    if entry.json_payload
                    else None,
                    resource_type=entry.resource.type,
                    resource_labels=dict(entry.resource.labels),
                    trace=entry.trace,
                    span_id=entry.span_id,
                )
            )
        return query_results
