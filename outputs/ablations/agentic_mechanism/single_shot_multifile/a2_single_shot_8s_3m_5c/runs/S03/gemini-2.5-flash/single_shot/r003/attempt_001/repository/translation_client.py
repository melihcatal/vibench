import os
from google.cloud import translate_v3 as translate

def get_translation_client() -> translate.TranslationServiceClient:
    return translate.TranslationServiceClient()

def get_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        try:
            from google.auth import default
            _, project_id = default()
        except Exception:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set and unable to infer from default credentials.")
    return project_id

def get_location() -> str:
    return os.getenv("GOOGLE_CLOUD_TRANSLATE_LOCATION", "global")
