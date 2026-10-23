import os
from google.cloud import monitoring_v3
from google.oauth2 import service_account


def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    credentials = None
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    return monitoring_v3.MetricServiceClient(credentials=credentials)