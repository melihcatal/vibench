import os
from dataclasses import dataclass

from google.cloud import translate_v3


@dataclass
class TranslationConfig:
    project_id: str
    location: str = "global"


def load_translation_config() -> TranslationConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return TranslationConfig(project_id=project_id, location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"))


def get_translation_client() -> translate_v3.TranslationServiceClient:
    return translate_v3.TranslationServiceClient()


def location_path(config: TranslationConfig) -> str:
    return f"projects/{config.project_id}/locations/{config.location}"
