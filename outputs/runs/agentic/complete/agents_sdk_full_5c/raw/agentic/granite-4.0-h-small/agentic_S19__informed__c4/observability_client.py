# [HELPER] observability_client.py
# Helper utilities for creating and configuring Managed Metrics Monitoring clients

from google.cloud import monitoring_v3
import os

# Expected env vars for Google Cloud Monitoring
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    """Return an authenticated MetricServiceClient.

    Uses Application Default Credentials or a service account JSON pointed to by
    GOOGLE_APPLICATION_CREDENTIALS. The client returns string identifiers suitable
    for helper functions in observability_models.
    """
    if CREDENTIALS_PATH:
        client = monitoring_v3.MetricServiceClient.from_service_account_json(CREDENTIALS_PATH)
    else:
        client = monitoring_v3.MetricServiceClient()
    return client
