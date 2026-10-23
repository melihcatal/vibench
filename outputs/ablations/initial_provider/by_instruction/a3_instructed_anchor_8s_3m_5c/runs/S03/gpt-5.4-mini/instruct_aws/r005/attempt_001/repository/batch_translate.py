from translation_client import translate_text_via_aws
from translation_models import TranslationRequest, TranslationResponse, normalize_text_list


def batch_translate(source_texts, source_language, target_language):
    texts = normalize_text_list(source_texts)
    responses = []
    for text in texts:
        request = TranslationRequest(text, source_language, target_language)
        translated = translate_text_via_aws(request.source_text, request.source_language, request.target_language)
        responses.append(TranslationResponse(translated, request.source_language, request.target_language, "aws.translate"))
    return responses
