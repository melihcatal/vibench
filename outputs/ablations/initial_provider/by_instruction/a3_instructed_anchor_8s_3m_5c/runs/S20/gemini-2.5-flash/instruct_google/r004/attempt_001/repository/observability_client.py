import os
from google.cloud import logging
from observability_models import StructuredLogEntry, CorrelatedLogEntry

class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None, log_name: str = "application-log"):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

        self.project_id = project_id
        self.log_name = log_name
        self.client = logging.Client(project=self.project_id)

    def write_log_entry(self, entry: StructuredLogEntry):
        logger = self.client.logger(self.log_name)
        logger.log_struct(
            info=entry.json_payload,
            severity=entry.severity.upper(),
            labels=entry.labels,
            resource=logging.Resource(type="global", labels={})
        )

    def write_correlated_log_entry(self, entry: CorrelatedLogEntry):
        logger = self.client.logger(self.log_name)
        logger.log_struct(
            info=entry.json_payload,
            severity=entry.severity.upper(),
            labels=entry.labels,
            resource=logging.Resource(type="global", labels={})
        )

    def query_logs(self, filter_string: str, order_by: str = "timestamp desc", limit: int = 100):
        # Google Cloud Logging filter strings are based on the Cloud Logging query language
        # Example: "severity=ERROR AND timestamp >= \"2023-01-01T00:00:00Z\""
        entries = self.client.list_entries(
            filter_=filter_string,
            order_by=order_by,
            page_size=limit
        )
        # Convert iterator to a list of dicts for easier processing
        return [entry.to_api_repr() for entry in entries]
