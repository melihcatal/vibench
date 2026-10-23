from typing import Optional, Dict, Any, List
from datetime import datetime
from google.cloud import logging as google_logging
from google.oauth2 import service_account
from observability_models import LogEntry, LogQuery, LogResponse
import os


class GoogleLoggingClient:
    def __init__(self, log_name: str = "application-logs"):
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = google_logging.Client(credentials=credentials)
        else:
            self.client = google_logging.Client()
        self.logger = self.client.logger(log_name)

    def write_log(self, log_entry: LogEntry) -> None:
        self.logger.log_struct(log_entry.to_dict())

    def write_logs(self, log_entries: List[LogEntry]) -> None:
        for entry in log_entries:
            self.write_log(entry)

    def query_logs(self, query: LogQuery) -> LogResponse:
        filter_str = ""
        if query.severity_filter:
            filter_str += " OR ".join([f"severity={s}" for s in query.severity_filter])
        if query.time_range_start and query.time_range_end:
            if filter_str:
                filter_str += " AND "
            filter_str += (
                f"timestamp>=\"{query.time_range_start.isoformat()}\" "
                f"timestamp<=\"{query.time_range_end.isoformat()}\""
            )
        for field, value in query.field_filters.items():
            if filter_str:
                filter_str += " AND "
            filter_str += f"{field}=\"{value}\""

        entries = list(self.logger.list_entries(filter_=filter_str))
        return LogResponse.from_google_logging(entries)