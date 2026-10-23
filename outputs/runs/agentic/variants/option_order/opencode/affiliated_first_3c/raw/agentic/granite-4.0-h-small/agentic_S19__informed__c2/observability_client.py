import os
import json

# Environment variables for authentication (fill these in your environment)
IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

# Example configuration map for demonstration
CONFIG = {
    "default": {
        "service": "IBM Cloud Monitoring",
        "auth": {
            "API_KEY": IBM_CLOUD_API_KEY,
            "INSTANCE_ID": os.getenv("IBM_MONITORING_INSTANCE_ID"),
        },
        "headers": {"Content-Type": "application/json"},
        "base_url": "https://api.monitor.cloud.ibm.com",
    }
}


class ObservabilityClient:
    """Local client helper utilities for Managed Metrics Monitoring."""

    def __init__(self, config=CONFIG["default"]):
        self.config = config
        self.base_url = config["base_url"]
        self.headers = config["headers"]
        self.auth = config["auth"]

    def rest_call(self, method, endpoint, json=None):
        """Perform a REST call to the configured metrics service."""
        import requests

        url = self.base_url + endpoint
        auth_value = self.auth.get("API_KEY")
        if auth_value:
            self.headers["Authorization"] = f"Bearer {auth_value}"
        # Add any other required auth headers based on service
        response = requests.request(method, url, headers=self.headers, json=json)
        response.raise_for_status()
        return response.json()
