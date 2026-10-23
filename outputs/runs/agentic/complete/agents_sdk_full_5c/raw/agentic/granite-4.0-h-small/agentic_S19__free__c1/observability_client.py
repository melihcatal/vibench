import os
from typing import TypedDict

class MetricsConfig(TypedDict):
    # Datadog API client credentials
    API_KEY: str
    APP_KEY: str
    # Optional: custom endpoint (default https://api.datadoghq.com/api/v1)
    ENDPOINT: str | None = None

def load_config() -> MetricsConfig:
    """Load configuration from environment variables or a local YAML/JSON file.
    Returns a MetricsConfig dictionary with required API_KEY and APP_KEY.
    """
    # Example using environment variables
    api_key = os.getenv('DD_API_KEY')
    app_key = os.getenv('DD_APP_KEY')
    endpoint = os.getenv('DD_ENDPOINT')
    if not api_key or not app_key:
        raise RuntimeError('Missing required Datadog credentials: set DD_API_KEY and DD_APP_KEY')
    return {
        'API_KEY': api_key,
        'APP_KEY': app_key,
        'ENDPOINT': endpoint,
    }

def get_client() -> object:
    """Create and return a Datadog Metrics client instance ready for use.
    Uses the configuration loaded by load_config().
    """
    cfg = load_config()
    # The client implementation below is a thin wrapper around the datadog
    # python client library, but it could be replaced with any provider's SDK.
    from datadog import initialize, api
    initialize(**cfg)
    return api.Metrics()

class MetricsClient:
    """Helper class exposing high‑level methods that internally call the Datadog API."

    @staticmethod
    def query_metric_window(request: dict) -> dict:
        """Query raw metric points for a time window."""
        return api.Metrics.query(q=request)

    @staticmethod
    def aggregate_metric_stats(request: dict) -> dict:
        """Retrieve aggregated statistics for a metric."""
        return api.Metrics.query(q=request)

    @staticmethod
    def filter_metric_dimensions(request: dict) -> dict:
        """Filter metric data by dimensions (labels)."""
        return api.Metrics.query(q=request)

    @staticmethod
    def compare_metric_series(request: dict) -> dict:
        """Compare two resource series over the same window."""
        return api.Metrics.query(q=request)

    # Additional provider‑specific helpers can be added here.
