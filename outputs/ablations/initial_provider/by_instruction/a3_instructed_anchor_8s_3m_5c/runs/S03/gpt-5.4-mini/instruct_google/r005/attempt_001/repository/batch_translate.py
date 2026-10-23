from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, parent_path
from translation_models import BatchTranslationRequest, coerce_language, normalize_text_list


def batch_translate(texts, source_language: str, target_language: str):
    request = BatchTranslationRequest(
        source_language=coerce_language(source_language),
        target_language=coerce_language(target_language),
        texts=normalize_text_list(texts),
    )
    client = get_translation_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": request.texts,
            "mime_type": request.mime_type,
            "source_language_code": request.source_language,
            "target_language_code": request.target_language,
        }
    )
    return [item.translated_text for item in response.translations]
