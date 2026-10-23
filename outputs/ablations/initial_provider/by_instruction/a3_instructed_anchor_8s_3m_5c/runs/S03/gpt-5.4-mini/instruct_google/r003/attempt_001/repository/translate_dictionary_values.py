from translation_client import translate_batch_google
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse, normalize_mapping, normalize_text


def translate_dictionary_values(values, source_language: str, target_language: str) -> DictionaryTranslationResponse:
    request = DictionaryTranslationRequest(
        values=normalize_mapping(values),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    keys = list(request.values.keys())
    translated = translate_batch_google(list(request.values.values()), request.source_language, request.target_language)
    translated_values = {key: item.get("translatedText", "") for key, item in zip(keys, translated)}
    return DictionaryTranslationResponse(translated_values=translated_values, provider="google", metadata={"results": translated})
