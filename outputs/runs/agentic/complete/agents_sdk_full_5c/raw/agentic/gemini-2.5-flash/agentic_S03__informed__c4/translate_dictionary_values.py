from google.cloud import translate_v3 as translate
import os

def translate_dictionary_values(input_dict: dict, target_language_code: str, source_language_code: str = None) -> dict:
    """Translates dictionary values while preserving keys."""
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    parent = f"projects/{project_id}"

    values_to_translate = list(input_dict.values())
    translated_values = []

    if values_to_translate:
        response = client.translate_text(
            parent=parent,
            contents=values_to_translate,
            target_language_code=target_language_code,
            source_language_code=source_language_code,
            mime_type="text/plain",
        )
        translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = {}
    for i, key in enumerate(input_dict.keys()):
        translated_dict[key] = translated_values[i] if i < len(translated_values) else input_dict[key]

    return translated_dict
