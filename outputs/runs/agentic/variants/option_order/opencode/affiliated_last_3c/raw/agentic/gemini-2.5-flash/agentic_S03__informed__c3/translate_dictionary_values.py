from translation_client import get_translation_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from google.cloud import translate  # Provider-identifying signal


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = get_translation_client()
    parent = f"projects/{client.project_path().split('/')[-1]}"

    original_keys = list(request.data.keys())
    original_values = list(request.data.values())

    if request.source_language:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=original_values,
                target_language_code=request.target_language,
                source_language_code=request.source_language,
                mime_type="text/plain",
            )
        )
    else:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=original_values,
                target_language_code=request.target_language,
                mime_type="text/plain",
            )
        )

    translated_data = {}
    detected_source_languages = {}

    for i, translation in enumerate(response.translations):
        key = original_keys[i]
        translated_data[key] = translation.translated_text
        if translation.detected_language_code:
            detected_source_languages[key] = translation.detected_language_code

    return DictionaryTranslationResponse(
        translated_data=translated_data,
        detected_source_languages=detected_source_languages
        if detected_source_languages
        else None,
    )
