import os
from google.cloud import translate

class TranslationResult:
    def __init__(self, translated_text: str, detected_language: str):
        self.translated_text = translated_text
        self.detected_language = detected_language

def translate_text(text: str, target_language_code: str, source_language_code: str = None) -> TranslationResult:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # The client will automatically pick up credentials from the environment.
    client = translate.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Or pass project_id directly
    if not project_id:
        # Attempt to get project ID from credentials if not explicitly set
        import google.auth
        credentials, project_id = google.auth.default()
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project ID from credentials not found.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )
    else:
        # Let the API detect the source language
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": target_language_code,
            }
        )

    translated_text = ""
    detected_language = ""

    if response.translations:
        translated_text = response.translations[0].translated_text
        # The detected language is only available when not explicitly set in the request
        if response.translations[0].detected_language_code:
            detected_language = response.translations[0].detected_language_code

    return TranslationResult(translated_text=translated_text, detected_language=detected_language)
