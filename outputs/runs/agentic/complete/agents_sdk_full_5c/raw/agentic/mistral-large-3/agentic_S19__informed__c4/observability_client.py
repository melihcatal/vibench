import os
from typing import Optional, Dict


def get_client_config() -> Dict[str, Optional[str]]:
    """Load configuration for Google Cloud Monitoring client."""
    return {
        "GOOGLE_CLOUD_PROJECT": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    }


def validate_metric_type(metric_type: str) -> bool:
    """Validate a Google Cloud Monitoring metric type string."""
    return metric_type.startswith("custom.googleapis.com/") or metric_type.startswith("compute.googleapis.com/")