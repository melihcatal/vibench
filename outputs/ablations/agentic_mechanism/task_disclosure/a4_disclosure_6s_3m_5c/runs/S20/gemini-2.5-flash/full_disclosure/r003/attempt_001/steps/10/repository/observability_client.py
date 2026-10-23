from google.cloud import logging_v2

class ObservabilityClient:
    def __init__(self, project_id: str, log_name: str):
        self.project_id = project_id
        self.log_name = log_name
        self.client = logging_v2.Client(project=self.project_id)

    def write_log_entry(self, json_payload: dict, severity: str = "INFO"):
        logger = self.client.logger(self.log_name)
        logger.log_struct(
            json_payload,
            severity=severity
        )
