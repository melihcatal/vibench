from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource

class ObservabilityClient:
    def __init__(self, project_id: str, log_name: str):
        self.project_id = project_id
        self.log_name = log_name
        self.client = logging_v2.Client(project=self.project_id)
        self.logger = self.client.logger(self.log_name)

    def write_log_entry(self, payload: dict, severity: str = "INFO", resource_type: str = "global", labels: dict = None):
        if labels is None:
            labels = {"project_id": self.project_id}
        
        # Google Cloud Logging expects 'jsonPayload' for structured logs
        # The `log_struct` method handles this automatically.
        self.logger.log_struct(
            payload,
            severity=severity,
            resource=Resource(type=resource_type, labels=labels),
        )
        return {"submitted": True}

    def list_log_entries(self, filter_expression: str, order_by: str = "timestamp desc", page_size: int = 100):
        entries = self.client.list_entries(
            filter_=filter_expression,
            order_by=order_by,
            page_size=page_size,
            project_ids=[self.project_id]
        )
        # Iterate over entries to retrieve all pages
        return [entry for entry in entries]

