from translation_client import create_translation_client, target_language_code
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_text_list


def batch_translate(source_language: str, target_language: str, texts: list[object]) -> BatchTranslationResponse:
    request = BatchTranslationRequest(source_language=source_language, target_language=target_language, texts=normalize_text_list(texts))
    client = create_translation_client()
    translated_texts = []
    for text in request.texts:
        result = client.translate_text(text, source_lang=target_language_code(request.source_language), target_lang=target_language_code(request.target_language))
        translated_texts.append(result.text)
    return BatchTranslationResponse(translated_texts=translated_texts)
