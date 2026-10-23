import os
from typing import Any, Dict

class ObservabilityAPIError(Exception):
    pass

def get_logging_client() -> Any:
    """Return a concrete managed logging service client.
    For illustration we use Datadog Logs via its Python SDK `datadog`.
    The client is configured via environment variables (DD_API_KEY, DD_APP_KEY).
    """
    try:
        from datadog import initialize, api
    except ImportError:
        raise ImportError("Please install the Datadog SDK: pip install datadog")

    # Minimal Datadog initialization from env vars
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DD_API_KEY and DD_APP_KEY must be set for Datadog client")

    initialize(api_key=api_key, app_key=app_key)
    # Expose Datadog's API client for log submission
    return api


def normalize_log_entry(entry: dict) -> dict:
    """
    Convert a raw log dict into a format expected by the provider.
    Handles timestamp conversion, flattens nested dicts, and ensures required fields.
    """
    norm = {
        "timestamp": entry.get("timestamp") or int((datetime.utcnow()).timestamp() * 1000),
        "message": entry.get("message", "")
    }
    # Flatten metadata while preserving provider-specific keys
    meta = {k: v for k, v in entry.items() if k not in ("timestamp", "message")}
    norm["ddtags"] = ",".join([f"{k}:{v}" for k, v in meta.items()])
    return norm


def post_process_response(resp: Any) -> list[dict]:
    """Normalize provider-specific response into a list of dicts for downstream steps."""
    # Datadog returns a list of log dicts under 'logs' key
    if isinstance(resp, dict) and "logs" in resp:
        return resp["logs"]
    # Fallback for generic response types
    return []

# Example minimal usage (will be removed in production)
if __name__ == "__main__":
    client = get_logging_client()
    # Query example using Datadog Logs Search API
    query = "@log:application AND @level:error"
    response = client.PostQuery(query=query, from_='-10m', to='now', type_='logs')
    logs = post_process_response(response)
    print('Queried logs count:', len(logs))