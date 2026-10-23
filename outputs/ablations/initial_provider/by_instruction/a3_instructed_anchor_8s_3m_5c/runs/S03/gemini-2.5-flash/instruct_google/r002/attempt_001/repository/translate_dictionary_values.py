from translation_client import get_translation_client
from translation_models import TranslationResponse
from google.cloud import translate_v3beta1 as translate

def translate_dictionary_values(data: dict, target_language: str, source_language: str = None) -> dict:
    client = get_translation_client()
    parent = f"projects/{{YOUR_PROJECT_ID}}/locations/global"

    # Extract values to translate
    values_to_translate = list(data.values())
    keys = list(data.keys())

    if not values_to_translate:
        return {}

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=values_to_translate,
            target_language_code=target_language,
            source_language_code=source_language if source_language else None,
            mime_type="text/plain",
        )
    )

    translated_data = {}
    for i, translation in enumerate(response.translations):
        translated_data[keys[i]] = translation.translated_text

    return translated_data
