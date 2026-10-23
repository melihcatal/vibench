from google.cloud import logging


class ObservabilityClient:
    def __init__(self, project_id: str = None):
        self.logging_client = logging.Client(project=project_id)

    def get_logger(self, log_name: str):
        return self.logging_client.logger(log_name)

    def get_logging_client(self):
        return self.logging_client
