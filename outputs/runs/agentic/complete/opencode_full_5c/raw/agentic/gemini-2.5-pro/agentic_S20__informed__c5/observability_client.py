import os
from google.cloud import logging


def get_gcp_logger(name: str):
    """Initializes and returns a Google Cloud Logging client."""

    # Make sure credentials are set
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        # Fallback for local development if project is not specified
        try:
            from google.cloud import core

            project_id = core.DefaultCredentials().project_id
        except Exception:
            raise EnvironmentError(
                "GCP_PROJECT_ID not set and could not be determined."
            )

    client = logging.Client(project=project_id)
    return client.logger(name)


def get_gcp_query_client():
    """Initializes and returns a Google Cloud Logging query client."""
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        try:
            from google.cloud import core

            project_id = core.DefaultCredentials().project_id
        except Exception:
            raise EnvironmentError(
                "GCP_PROJECT_ID not set and could not be determined."
            )

    # Using the google.cloud.logging_v2 client for querying
    from google.cloud import logging_v2

    client = logging_v2.services.logging_service_v2.LoggingServiceV2Client()
    return client, project_id
