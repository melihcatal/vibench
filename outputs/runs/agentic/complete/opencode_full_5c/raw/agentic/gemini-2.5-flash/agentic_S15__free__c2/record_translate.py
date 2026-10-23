from database_client import get_translate_client
from typing import Dict, Any


def translate_record_field(
    text_content: str, source_language: str, target_language: str
) -> Dict[str, Any]:
    """
    Translates user-facing text content from a document record using AWS Translate.

    Args:
        text_content: The text field of a document record to translate.
        source_language: The source language code (e.g., 'en', 'es').
        target_language: The target language code (e.g., 'fr', 'de').

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    translate_client = get_translate_client()

    translation_results = {"translated_text": "", "detected_source_language": "unknown"}

    if not text_content or not isinstance(text_content, str):
        return translation_results

    try:
        response = translate_client.translate_text(
            Text=text_content,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        if response:
            translation_results["translated_text"] = response["TranslatedText"]
            translation_results["detected_source_language"] = response[
                "SourceLanguageCode"
            ]

    except Exception as e:
        print(f"Error translating text with AWS Translate: {e}")

    return translation_results
