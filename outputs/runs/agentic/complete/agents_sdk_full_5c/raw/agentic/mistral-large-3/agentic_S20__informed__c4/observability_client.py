import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.cloud import logging as google_logging
from google.cloud.logging_v2 import Client as GoogleLoggingClient
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.oauth2 import service_account
from observability_models import LogEntry, LogQueryRequest, LogQueryResponse, NormalizedLogEntry


class GoogleCloudLoggingClient:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.client: GoogleLoggingClient = google_logging.Client(credentials=self.credentials)
        self.logger = self.client.logger(os.getenv("GOOGLE_LOG_NAME", "application-logs"))

    def write_log(self, log_entry: LogEntry) -> None:
        self.logger.log_struct(log_entry.to_dict())

    def write_logs(self, log_entries: List[LogEntry]) -> None:
        for entry in log_entries:
            self.write_log(entry)

    def query_logs(self, query_request: LogQueryRequest) -> LogQueryResponse:
        filter_parts = []
        if query_request.filter_severity:
            filter_parts.append(" OR ".join([f"severity={s}" for s in query_request.filter_severity]))
        if query_request.correlation_id:
            filter_parts.append(f"jsonPayload.correlation_id=\"{query_request.correlation_id}\"")
        if query_request.time_from:
            filter_parts.append(f"timestamp>=\"{query_request.time_from.isoformat()}Z\"")
        if query_request.time_to:
            filter_parts.append(f"timestamp<=\"{query_request.time_to.isoformat()}Z\"")

        filter_str = " AND ".join(filter_parts) if filter_parts else ""

        entries = []
        for entry in self.client.list_entries(
            filter_=filter_str,
            max_results=query_request.limit,
            order_by=google_logging.DESCENDING
        ):
            entries.append(NormalizedLogEntry.from_google_logging(entry).dict())

        return LogQueryResponse(entries=entries, total_count=len(entries))