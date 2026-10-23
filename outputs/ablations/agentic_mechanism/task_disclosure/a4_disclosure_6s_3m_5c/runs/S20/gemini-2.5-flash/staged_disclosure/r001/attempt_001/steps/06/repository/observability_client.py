import os
import json
import requests

class ObservabilityClient:
    def __init__(self):
        self._configure()

    def _configure(self):
        # Configuration for the observability service.
        # These would typically be specific to a managed logging/observability provider.
        self.api_key = os.getenv("OBSERVABILITY_API_KEY")
        self.endpoint = os.getenv("OBSERVABILITY_ENDPOINT", "https://api.observability.example.com")

        if not self.api_key:
            raise ValueError("OBSERVABILITY_API_KEY environment variable not set.")

        print(f"Observability client configured with endpoint: {self.endpoint}")

    def ingest_log(self, log_entry: dict) -> dict:
        """
        Ingests a single log entry into the managed observability service.
        This is a placeholder for actual service integration.
        """
        if not isinstance(log_entry, dict):
            raise TypeError("log_entry must be a dictionary.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        ingest_url = f"{self.endpoint}/logs/ingest" # Example endpoint

        try:
            response = requests.post(ingest_url, headers=headers, data=json.dumps(log_entry))
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error ingesting log: {e}")
            raise

    def query_logs(self, query: str, start_time: str, end_time: str) -> dict:
        """
        Queries logs from the managed observability service.
        This is a placeholder for actual service integration.
        """
        if not all(isinstance(arg, str) for arg in [query, start_time, end_time]):
            raise TypeError("query, start_time, and end_time must be strings.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        query_url = f"{self.endpoint}/logs/query" # Example endpoint
        payload = {
            "query": query,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            response = requests.get(query_url, headers=headers, params=payload)
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying logs: {e}")
            raise
