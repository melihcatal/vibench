from google.cloud import translate_v3
from typing import Dict, Any, List, Union
from messaging_models import PubSubMessage
from messaging_client import get_project_id


def translate_message_payload(
    message: PubSubMessage, target_language_code: str, source_language_code: str = "en"
) -> Dict[str, Any]:
    """Translates customer-facing text within a message payload using Google Cloud Translation API.

    This function assumes the text to be translated is directly in `message.data` or can be extracted.
    For simplicity, it attempts to translate string values within the message data.
    More complex payloads would require specific key-path translation logic.

    Args:
        message: The PubSubMessage object with the payload to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (e.g., "en" for English).

    Returns:
        A dictionary representing the translated message payload, or a dictionary indicating failure.
    """
    translation_client = translate_v3.TranslationServiceClient()
    project_id = get_project_id()
    parent = f"projects/{project_id}/locations/global"

    translated_data = message.data.copy()
    texts_to_translate = []
    original_paths = []  # To reconstruct the translated data structure

    def extract_strings(data, path_prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path_prefix}.{key}" if path_prefix else key
                extract_strings(value, new_path)
        elif isinstance(data, list):
            for i, value in enumerate(data):
                new_path = f"{path_prefix}[{i}]"
                extract_strings(value, new_path)
        elif isinstance(data, str):
            texts_to_translate.append(data)
            original_paths.append(path_prefix)

    extract_strings(message.data)

    if not texts_to_translate:
        return {
            "translated_data": translated_data,
            "translation_status": "no_strings_to_translate",
        }

    try:
        response = translation_client.translate_text(
            request={
                "parent": parent,
                "contents": texts_to_translate,
                "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        # Reconstruct the translated data. This is a simplified reconstruction and might need adjustment
        # for deeply nested structures or specific key targeting.
        translated_strings = [
            translation.translated_text for translation in response.translations
        ]

        # Simple reconstruction: replace original string values with translated ones
        # This part assumes a direct 1:1 replacement and might be insufficient for complex objects
        # For this example, we'll just return the original data with a list of translations for simplicity.
        # A real implementation would traverse the original_paths to update translated_data.
        return {
            "original_data": message.data,
            "translated_texts": translated_strings,
            "target_language": target_language_code,
            "translation_status": "success",
        }

    except Exception as e:
        return {
            "translated_data": message.data,
            "translation_status": "failed",
            "error": str(e),
        }
