from google.cloud import monitoring_v3
from google.oauth2 import service_account
import os

def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    )
    return monitoring_v3.MetricServiceClient(credentials=credentials)