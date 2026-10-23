from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse


def translate_dictionary_values(payload: DictionaryTranslationRequest, config: dict = None) -> DictionaryTranslationResponse:
    config = config or {}
    client = TranslationClient(project_id=config.get('project_id'), location=config.get('location'))

    keys = list(payload.dictionary.keys())
    values_to_translate = list(payload.dictionary.values())

    if not values_to_translate:
        return DictionaryTranslationResponse(
            translated_dictionary={},
            source_language=payload.source_language,
            target_language=payload.target_language,
        )

    response = client.client.translate_text(request={
        "parent": client.parent,
        "contents": values_to_translate,
        "mime_type": "text/plain",
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dictionary = dict(zip(keys, translated_values))

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dictionary,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
