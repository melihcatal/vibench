import os
import requests
import json

class ObservabilityClient:
    def __init__(self, api_key: str = None, service_endpoint: str = None):
        self.api_key = api_key if api_key else os.getenv("OBSERVABILITY_API_KEY")
        self.service_endpoint = service_endpoint if service_endpoint else os.getenv("OBSERVABILITY_SERVICE_ENDPOINT", "https://logs.example.com/api/v1")

        if not self.api_key:
            raise ValueError("API Key not provided and OBSERVABILITY_API_KEY environment variable not set.")
        if not self.service_endpoint:
            raise ValueError("Service endpoint not provided and OBSERVABILITY_SERVICE_ENDPOINT environment variable not set.")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def ingest_log(self, log_event: dict):
        """
        Ingests a single structured log event into the managed logging service.
        """
        if not isinstance(log_event, dict):
            raise TypeError("log_event must be a dictionary.")

        try:
            response = requests.post(f"{self.service_endpoint}/ingest", headers=self.headers, data=json.dumps(log_event))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error ingesting log: {e}")
            raise

    def query_logs(self, query_params: dict):
        """
        Queries logs from the managed logging service.
        """
        if not isinstance(query_params, dict):
            raise TypeError("query_params must be a dictionary.")

        try:
            response = requests.get(f"{self.service_endpoint}/query", headers=self.headers, params=query_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying logs: {e}")
            raise
