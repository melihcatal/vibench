import os
from typing import Any, Dict


def get_log_client() -> Any:
    """Instantiate and return a provider‑specific log ingestion client.

    The choice of provider is driven by environment variables (see the docs for
    each provider). This helper abstracts away the SDK import and authentication
    details for the rest of the application.
    """
    # --- Example: using Amazon CloudWatch (boto3) ---
    try:
        import boto3

        # CloudWatch Logs client
        client = boto3.client(
            service_name="logs", region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        # boto3 client is a valid provider instance for our other functions
        return client
    except ImportError:
        # --- Fallback to Datadog REST API (requests) ---
        import requests

        dd_api_key = os.getenv("DD_API_KEY")
        dd_app_key = os.getenv("DD_APP_KEY")
        base_url = "https://api.datadoghq.com/api/v1/logs"
        headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": dd_api_key,
            "DD-APPLICATION-KEY": dd_app_key,
        }

        class DatadogClient:
            def send_log(self, payload: str) -> None:
                requests.post(f"{base_url}-logs", headers=headers, data=payload)

            def send_logs(self, payload: str) -> None:
                requests.post(f"{base_url}-logs/batch", headers=headers, data=payload)

            def search_logs(self, filters: Dict) -> Dict:
                # Simple GET search example (Datadog Logs Search API)
                search_params = {
                    "query": f"{filters['severity']} AND timestamp>{filters['timestamp_range']['start']}",
                    "from": filters["timestamp_range"]["start"],
                    "to": filters["timestamp_range"]["end"],
                }
                resp = requests.get(
                    f"{base_url}-search", params=search_params, headers=headers
                )
                return resp.json()

        return DatadogClient()
    # Add additional provider blocks as needed (OpenTelemetry Collector, Splunk, etc.)
