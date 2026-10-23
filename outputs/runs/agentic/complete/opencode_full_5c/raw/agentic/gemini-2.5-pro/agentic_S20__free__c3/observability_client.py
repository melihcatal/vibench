from google.cloud import logging_v2
import os


def get_logging_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = logging_v2.LoggingServiceV2Client()
    return client, f"projects/{project_id}"


def get_log_sink_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = logging_v2.ConfigServiceV2Client()
    return client, f"projects/{project_id}"


def get_logger(log_name="my-app-log"):
    client = logging_v2.LoggingServiceV2Client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    logger = client.logger(log_name, project=project_id)
    return logger


class CloudLoggingClient:
    def __init__(self, project_id: str = None):
        if project_id is None:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

        self.project_id = project_id
        self.client = logging_v2.LoggingServiceV2Client()
        self.project_name = f"projects/{self.project_id}"

    def list_entries(self, filter_str: str, limit: int = 10):
        return self.client.list_log_entries(
            resource_names=[self.project_name], filter_=filter_str, page_size=limit
        )
