from translation_client import translate_batch_google
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_sequence, normalize_text


def batch_translate(texts, source_language: str, target_language: str) -> BatchTranslationResponse:
    request = BatchTranslationRequest(
        texts=normalize_sequence(texts),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    results = translate_batch_google(request.texts, request.source_language, request.target_language)
    translated_texts = [item.get("translatedText", "") for item in results]
    return BatchTranslationResponse(translated_texts=translated_texts, provider="google", metadata={"results": results})
