from messaging_client import get_translation_client, PROJECT_ID, TRANSLATION_LOCATION
from google.cloud.translate_v3 import (
    TranslationServiceClient,
)  # Explicit import for provider signal


def translate_message_text(
    text: str, target_language_code: str, source_language_code: str = "en"
) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation API."""
    client = get_translation_client()
    parent = f"projects/{PROJECT_ID}/locations/{TRANSLATION_LOCATION}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # The response contains a list of translations.
    for translation in response.translations:
        return translation.translated_text
    return text  # Return original text if no translation occurs (e.g., empty response)
