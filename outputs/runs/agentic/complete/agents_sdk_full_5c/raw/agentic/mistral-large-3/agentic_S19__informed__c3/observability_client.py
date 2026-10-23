import os
from typing import Dict, Any

def get_client_config() -> Dict[str, Any]:
    """
    Load configuration for Google Cloud Monitoring.
    Requires GOOGLE_APPLICATION_CREDENTIALS or explicit project_id.
    """
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID", ""),
    }

def validate_metric_type(metric_type: str) -> bool:
    """Validate Google Cloud Monitoring metric type format."""
    return metric_type.startswith("custom.googleapis.com/") or metric_type.startswith("compute.googleapis.com/")