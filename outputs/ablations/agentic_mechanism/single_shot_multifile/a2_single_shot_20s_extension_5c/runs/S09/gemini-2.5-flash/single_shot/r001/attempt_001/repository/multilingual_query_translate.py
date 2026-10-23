import os
from google.cloud import translate_v3 as translate

def translate_query_google_cloud(text: str, target_language_code: str, project_id: str = None) -> str:
    """
    Translates a query text into a specified target language using Google Cloud Translation API.
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set or gcloud auth is configured.
    """
    client = translate.TranslationServiceClient()

    if project_id is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set or project_id not provided.")

    location = os.environ.get("GCP_LOCATION", "global") # Global is common for Translation API
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )
        for translation in response.translations:
            return translation.translated_text
        return text # Should not happen if response is valid
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return text # Return original text on failure
