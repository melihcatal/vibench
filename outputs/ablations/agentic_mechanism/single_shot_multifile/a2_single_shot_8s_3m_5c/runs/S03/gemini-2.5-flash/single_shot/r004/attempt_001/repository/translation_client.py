import os
from google.cloud import translate_v3beta1 as translate

def get_translation_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return translate.TranslationServiceClient()

def get_location_path(project_id, location):
    return f"projects/{project_id}/locations/{location}"