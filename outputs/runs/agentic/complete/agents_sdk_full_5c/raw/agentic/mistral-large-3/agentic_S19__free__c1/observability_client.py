import os
from typing import Dict, Any


def get_client_config() -> Dict[str, Any]:
    """Load configuration for Google Cloud Monitoring client."""
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }


def validate_environment() -> None:
    """Ensure required environment variables are set for Google Cloud Monitoring."""
    required_vars = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS"]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")