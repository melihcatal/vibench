# observability_client.py
# Helper utilities for Managed Metrics Monitoring

import os


class ObservabilityClient:
    """Provides configuration and client helper utilities for various monitoring services."""

    _clients = {}

    @staticmethod
    def get_client(service):
        if service in ObservabilityClient._clients:
            return ObservabilityClient._clients[service]
        # Simple config via env vars (example)
        client = None
        if service == "datadog":
            api_key = os.getenv("DD_API_KEY")
            app_key = os.getenv("DD_APP_KEY")
            client = {"service": "datadog", "api_key": api_key, "app_key": app_key}
        elif service == "google":
            client = {
                "service": "google",
                "credentials": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            }
        elif service == "aws":
            client = {
                "service": "aws",
                "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
                "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            }
        else:
            raise ValueError(f"Unsupported service for client creation: {service}")
        ObservabilityClient._clients[service] = client
        return client
