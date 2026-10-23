import os
from google.cloud import translate_v3 as translate

def get_translation_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return translate.TranslationServiceClient()

def get_location_path(project_id: str, location: str = "global") -> str:
    return translate.TranslationServiceClient.location_path(project_id, location)
