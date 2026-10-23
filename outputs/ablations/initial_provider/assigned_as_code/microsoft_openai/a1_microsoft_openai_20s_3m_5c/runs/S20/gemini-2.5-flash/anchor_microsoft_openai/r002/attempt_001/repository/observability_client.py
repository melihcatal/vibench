from google.cloud import logging
import os

class ObservabilityClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.logging_client = logging.Client(project=self.project_id)

    def write_log_entry(self, entry):
        logger = self.logging_client.logger(name=entry.resource_type)
        if entry.json_payload:
            logger.log_struct(entry.json_payload, severity=entry.severity, labels=entry.labels, resource=logging.Resource(type=entry.resource_type, labels={"resource_id": entry.resource_id}))
        elif entry.text_payload:
            logger.log_text(entry.text_payload, severity=entry.severity, labels=entry.labels, resource=logging.Resource(type=entry.resource_type, labels={"resource_id": entry.resource_id}))
        else:
            # Default to text payload if neither json_payload nor text_payload is provided
            logger.log_text(entry.message, severity=entry.severity, labels=entry.labels, resource=logging.Resource(type=entry.resource_type, labels={"resource_id": entry.resource_id}))

    def list_log_entries(self, filter_string: str, order_by: str = "timestamp desc", page_size: int = 100, page_token: str = None):
        entries = self.logging_client.list_entries(
            filter_=filter_string,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
            project_ids=[self.project_id]
        )
        return entries
