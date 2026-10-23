import os
from google.cloud import logging

class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.project_id = project_id
        self.logging_client = logging.Client(project=self.project_id)

    def get_logger(self, log_name: str):
        return self.logging_client.logger(log_name)

    def write_log_entry(self, log_name: str, message: str, severity: str, labels: Optional[Dict[str, str]] = None,
                        json_payload: Optional[Dict[str, Any]] = None):
        logger = self.get_logger(log_name)
        if json_payload:
            logger.log_struct(json_payload, severity=severity, labels=labels)
        else:
            logger.log_text(message, severity=severity, labels=labels)
