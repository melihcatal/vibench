from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResult, normalize_language_code


def batch_translate(texts, source_language, target_language, model=None):
    client = get_translation_client(model=model)
    request = BatchTranslationRequest(texts=list(texts), source_language=normalize_language_code(source_language), target_language=normalize_language_code(target_language))
    return BatchTranslationResult.from_provider_response(client.batch_translate(request))
