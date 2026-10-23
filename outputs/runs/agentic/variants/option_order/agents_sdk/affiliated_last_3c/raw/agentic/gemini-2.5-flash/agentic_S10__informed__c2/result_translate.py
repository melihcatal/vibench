import os
from google.cloud import translate

def translate_text(text: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID") # Or derive from GOOGLE_APPLICATION_CREDENTIALS

    if not project_id:
        # As a fallback, try to get project ID from credentials or environment if not explicitly set.
        # For simplicity, assume project_id is needed if not relying solely on GOOGLE_APPLICATION_CREDENTIALS default project.
        # For direct use with `google-cloud-translate` default behavior, project_id in client constructor is often optional.
        pass

    # The parent format is `projects/{project_id}/locations/{location_id}`.
    # Using 'global' for location_id is common.
    parent = f"projects/{project_id}/locations/global" if project_id else "projects/-/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
