import os
from google.cloud import translate_v2 as translate

from identity_client import get_google_application_credentials, get_google_cloud_project


def translate_consent_copy(text: str, target_language: str = "es") -> str:
    """Translates identity-provider consent copy using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to a service account key file
    # The client library will automatically use this if set.
    # For this example, we're assuming the environment variable is configured.
    _ = get_google_application_credentials()  # Ensure env var is loaded
    project_id = get_google_cloud_project()  # Ensure project ID is loaded

    translate_client = translate.Client(project=project_id)

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        return f"Error translating consent copy: {e}"
