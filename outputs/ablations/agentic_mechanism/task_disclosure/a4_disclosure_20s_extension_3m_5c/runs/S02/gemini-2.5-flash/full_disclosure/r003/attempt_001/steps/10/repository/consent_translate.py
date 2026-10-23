
from google.cloud import translate

def translate_consent_copy(text: str, target_language: str) -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    return response.translations[0].translated_text
