import os
from google.cloud import translate_v3


def get_translation_client():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        return translate_v3.TranslationServiceClient.from_service_account_file(
            credentials_path
        )
    return translate_v3.TranslationServiceClient()


def get_project_id():
    return os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("PROJECT_ID", ""))


def get_parent_location():
    project_id = get_project_id()
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    return f"projects/{project_id}/locations/{location}"


GOOGLE_TRANSLATE_MODEL = "nmt"
GOOGLE_TRANSLATE_API_ENDPOINT = "translate.googleapis.com"
