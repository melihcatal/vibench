import os
from typing import Optional

def get_google_cloud_project() -> str:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required.")
    return project

def get_default_logger_name(service: Optional[str] = None) -> str:
    return f"{service or 'app'}-logs"
