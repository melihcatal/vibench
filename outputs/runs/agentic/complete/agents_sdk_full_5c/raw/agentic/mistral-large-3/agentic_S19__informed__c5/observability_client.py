import os
from typing import Optional, Dict


def get_client_config() -> Dict[str, Optional[str]]:
    return {
        "GOOGLE_CLOUD_PROJECT": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }


def validate_config(config: Dict[str, Optional[str]]) -> None:
    if not config.get("GOOGLE_CLOUD_PROJECT"):
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required.")