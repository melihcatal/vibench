import os
from google.cloud import translate_v3 as translate

# Instantiates a client
_translate_client = None
def get_translate_client():
    global _translate_client
    if _translate_client is None:
        # Assumes GOOGLE_APPLICATION_CREDENTIALS or default ADC is set
        _translate_client = translate.TranslationServiceClient()
    return _translate_client

def translate_log_message(project_id: str, message_text: str, target_language_code: str = "es", source_language_code: str = "en") -> str:
    client = get_translate_client()

    location = "global" # Google Cloud Translation API typically uses 'global' for basic translations
    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from source_language_code to target_language_code.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [message_text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # Display the translation for the first response.
    if response.translations:
        return response.translations[0].translated_text
    return message_text # Return original if no translation found

