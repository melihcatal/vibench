from typing import Dict, Any, Optional, List
from datetime import datetime
import os
from google.cloud import logging as google_logging
from google.oauth2 import service_account
from observability_models import LogEntry, LogQuery, LogResponse


class GoogleLoggingClient:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.client = google_logging.Client(credentials=credentials)
        self.logger = self.client.logger("application_logs")

    def write_log(self, log_entry: LogEntry) -> None:
        self.logger.log_struct(log_entry.to_dict())

    def write_logs(self, log_entries: List[LogEntry]) -> None:
        self.logger.log_struct([entry.to_dict() for entry in log_entries])

    def query_logs(self, log_query: LogQuery) -> LogResponse:
        filter_parts = []
        if log_query.filter_severity:
            filter_parts.append(f"severity={log_query.filter_severity}")
        if log_query.time_from:
            filter_parts.append(f"timestamp>=\"{log_query.time_from.isoformat()}Z\"")
        if log_query.time_to:
            filter_parts.append(f"timestamp<=\"{log_query.time_to.isoformat()}Z\"")
        for key, value in log_query.custom_filters.items():
            filter_parts.append(f"{key}:{value}")
        filter_str = " AND ".join(filter_parts)

        entries = []
        for entry in self.client.list_entries(filter_=filter_str, max_results=1000):
            entries.append(entry)
        return LogResponse.from_google_logging(entries)