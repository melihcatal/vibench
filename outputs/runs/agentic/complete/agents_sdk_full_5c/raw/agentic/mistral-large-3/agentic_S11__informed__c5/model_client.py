import os
from typing import Dict, Any

def get_platform_config() -> Dict[str, str]:
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    }

def get_auth_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {os.getenv('GOOGLE_APPLICATION_CREDENTIALS_TOKEN')}"}