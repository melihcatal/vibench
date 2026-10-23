import os
from typing import Any, Dict, Optional


def get_google_credentials_path() -> Optional[str]:
    value = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    return value if value else None


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")


def get_location() -> str:
    return os.getenv("GOOGLE_CLOUD_LOCATION", "us")


def get_default_bucket() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")


def build_google_speech_config(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    config: Dict[str, Any] = {
        "encoding": "LINEAR16",
        "model": "latest_long",
        "features": {},
    }
    if overrides:
        config.update(overrides)
    return config
