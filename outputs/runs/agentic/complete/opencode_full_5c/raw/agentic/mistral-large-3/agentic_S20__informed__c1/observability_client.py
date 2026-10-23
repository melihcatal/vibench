import os
from google.cloud import logging as cloud_logging
from google.oauth2 import service_account


def get_logging_client():
    """
    Initializes and returns a Google Cloud Logging client.

    Returns:
        A configured Google Cloud Logging client.
    """
    credentials = None

    # Load credentials from environment variable if provided
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
        credentials_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )

    return cloud_logging.Client(credentials=credentials)


def normalize_log_payload(payload: dict) -> dict:
    """
    Normalizes a log payload to ensure it meets Google Cloud Logging requirements.

    Args:
        payload: Dictionary containing log data.

    Returns:
        Normalized log payload.
    """
    normalized = payload.copy()

    # Ensure all values are JSON-serializable
    for key, value in normalized.items():
        try:
            json.dumps(value)
        except (TypeError, ValueError):
            normalized[key] = str(value)

    return normalized
