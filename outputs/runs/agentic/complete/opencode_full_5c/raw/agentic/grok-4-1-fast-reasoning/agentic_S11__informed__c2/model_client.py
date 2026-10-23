import os
from typing import Dict, Any


def load_platform_config() -> Dict[str, Any]:
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "location": os.getenv("VERTEXAI_LOCATION", "us-central1"),
    }
