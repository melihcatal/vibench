import os
import logging
from google.cloud import logging as cloud_logging
from google.cloud.logging_v2.client import Client as LoggingClient

class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.logging_client: LoggingClient = cloud_logging.Client(project=self.project_id)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    def ingest_log(self, log_name: str, message: str, severity: str = "INFO", labels: dict = None):
        logger = self.logging_client.logger(log_name)
        logger.log(message, severity=severity, labels=labels)
        self.logger.info(f"Ingested log to {log_name} with message: {message}")

    def query_logs(self, filter_string: str, order_by: str = "timestamp desc", limit: int = 100):
        # Example filter: 'resource.type="cloud_run_revision" AND resource.labels.service_name="your-service"'
        # See: https://cloud.google.com/logging/docs/view/advanced-queries
        entries = self.logging_client.list_entries(
            filter_=filter_string,
            order_by=order_by,
            page_size=limit
        )
        logs = []
        for entry in entries:
            logs.append(entry.as_json())
        self.logger.info(f"Queried {len(logs)} logs with filter: {filter_string}")
        return logs
