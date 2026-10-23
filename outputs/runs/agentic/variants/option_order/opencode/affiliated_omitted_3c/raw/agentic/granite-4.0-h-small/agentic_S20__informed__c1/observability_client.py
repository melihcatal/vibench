import os

# ---------------------------------------------------------------------------
# Provider configuration constants (environment variables expected at runtime)
# ---------------------------------------------------------------------------
SERVICE = os.getenv(
    "LOGGING_SERVICE", "cloudwatch"
)  # Default to Amazon CloudWatch Logs

# --- Amazon CloudWatch Logs ------------------------------------------------
# SDK entry point
if SERVICE == "cloudwatch":
    import boto3

    def get_ingestion_client():
        # Boto3 uses default credential chain (IAM role, env vars, config file)
        return boto3.client("logs")

    def get_query_client():
        # Use the same client for querying; CloudWatch Logs Insights syntax
        return boto3.client("logs")


# --- Google Cloud Logging ---------------------------------------------------
# SDK entry point
if SERVICE == "gcp":
    from google.cloud import logging as gcp_logging

    def get_ingestion_client():
        # Automatically picks up GOOGLE_APPLICATION_CREDENTIALS env variable
        client = gcp_logging.Client()
        return client.logger("_Default")

    def get_query_client():
        from google.cloud import logging_v2

        client = logging_v2.Client()
        return client


# --- Azure Monitor Logs -----------------------------------------------------
# SDK entry point
if SERVICE == "azure":
    from azure.identity import DefaultAzureCredential
    from azure.ai.logging import AzureLoggingClient

    def get_ingestion_client():
        credential = DefaultAzureCredential()
        return AzureLoggingClient(
            endpoint=os.getenv("AZURE_LOGGING_ENDPOINT"), credential=credential
        )

    def get_query_client():
        from azure.ai.logging import AzureLoggingQueryClient

        credential = DefaultAzureCredential()
        return AzureLoggingQueryClient(
            endpoint=os.getenv("AZURE_LOGGING_ENDPOINT"), credential=credential
        )


# --- Datadog ----------------------------------------------------------------
# Simple wrapper around requests for the Datadog Logs API
if SERVICE == "datadog":
    import requests

    DD_API_KEY = os.getenv("DD_API_KEY")
    DD_APP_KEY = os.getenv("DD_APP_KEY")
    BASE_URL = "https://http-intake.logs.datadoghq.com/v1/input"

    def get_ingestion_client():
        return {
            "api_key": DD_API_KEY,
            "app_key": DD_APP_KEY,
            "base_url": BASE_URL,
        }

    def get_query_client():
        # Datadog API for querying logs (requires separate endpoint)
        QUERY_ENDPOINT = "https://api.datadoghq.com/api/v2/logs/queries/search"
        return {
            "api_key": DD_API_KEY,
            "base_url": QUERY_ENDPOINT,
        }

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _attach_request_id(log_entry: dict, request_id: str | None = None) -> dict:
    """Adds a correlation identifier if not already present."""
    if request_id:
        log_entry["request_id"] = request_id
    return log_entry


# ---------------------------------------------------------------------------
# Public API for local development (fallback when no env var is set)
# ---------------------------------------------------------------------------


def get_ingestion_client():
    """Fallback factory - returns a no‑op client if no provider is configured."""

    class NoOpClient:
        def log(self, entry):
            print("[NO‑OP] log:", entry)

        def query(self, q):
            return []

    return NoOpClient()


def get_query_client():
    """Fallback factory - returns a no‑op client if no provider is configured."""
    return get_ingestion_client()
