import os
from google.cloud import logging
from google.cloud.logging_v2.services import logging_service_v2
from google.cloud.logging_v2.types import ListLogEntriesRequest
from observability_models import LogEntry


class ObservabilityClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

        self.logging_client = logging.Client(project=self.project_id)
        self.query_client = logging_service_v2.LoggingServiceV2Client()

    def get_logger(self, name: str):
        return self.logging_client.logger(name)

    def write_log_entry(self, logger_name: str, log_entry: LogEntry):
        logger = self.get_logger(logger_name)

        payload = {"message": log_entry.message, "request_id": log_entry.request_id}
        if log_entry.extra_data:
            payload.update(log_entry.extra_data)

        logger.log_struct(payload, severity=log_entry.severity)

    def query_logs(self, filter_str: str, limit: int = 100):
        request = ListLogEntriesRequest(
            resource_names=[f"projects/{self.project_id}"],
            filter=filter_str,
            page_size=limit,
        )

        entries = self.query_client.list_log_entries(request=request)
        return entries
