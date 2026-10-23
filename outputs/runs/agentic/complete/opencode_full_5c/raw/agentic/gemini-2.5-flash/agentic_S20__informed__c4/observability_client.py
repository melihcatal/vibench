import os
from google.cloud import logging_v2


def get_logging_client():
    return logging_v2.Client()


def get_logger(log_name: str):
    client = get_logging_client()
    return client.logger(log_name)


def get_project_id():
    # Attempt to get project ID from GOOGLE_CLOUD_PROJECT environment variable
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback to default project from client if not explicitly set
        try:
            client = get_logging_client()
            project_id = client.project
        except Exception:
            pass
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable."
        )
    return project_id
