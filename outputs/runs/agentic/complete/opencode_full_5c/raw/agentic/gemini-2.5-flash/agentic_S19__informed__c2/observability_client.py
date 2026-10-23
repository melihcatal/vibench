from google.cloud import monitoring_v3
from google.oauth2 import service_account
import os


def get_monitoring_client():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client = monitoring_v3.MetricServiceClient(credentials=credentials)
    else:
        client = monitoring_v3.MetricServiceClient()
    return client
