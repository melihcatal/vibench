from translation_client import get_default_source_language, get_default_target_language, get_translation_client
from translation_models import BatchTranslationRequest, TranslationResponse, normalize_text_list


def batch_translate(texts, source_language=None, target_language=None):
    request = BatchTranslationRequest(
        texts=normalize_text_list(texts),
        source_language=source_language or get_default_source_language(),
        target_language=target_language or get_default_target_language(),
    )
    client = get_translation_client()
    result = client.translate(request.texts, source_language=request.source_language, target_language=request.target_language)
    if isinstance(result, dict):
        result = [result]
    return [
        TranslationResponse(
            translated_text=item["translatedText"],
            source_language=request.source_language,
            target_language=request.target_language,
            provider="google-cloud-translate-v2",
        )
        for item in result
    ]
