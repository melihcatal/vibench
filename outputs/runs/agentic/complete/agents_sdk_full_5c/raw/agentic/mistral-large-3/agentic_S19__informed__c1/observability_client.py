from google.cloud import monitoring_v3
from google.oauth2 import service_account
import os


class ObservabilityClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.client = monitoring_v3.MetricServiceClient(credentials=credentials)
        self.query_client = monitoring_v3.QueryServiceClient(credentials=credentials)

    def query_time_series(self, name: str, query: str):
        return self.query_client.query_time_series(name=name, query=query)


def get_observability_client() -> ObservabilityClient:
    return ObservabilityClient()