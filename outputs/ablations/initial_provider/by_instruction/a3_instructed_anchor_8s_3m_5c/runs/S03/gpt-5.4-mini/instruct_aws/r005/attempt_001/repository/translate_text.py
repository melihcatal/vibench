from translation_client import translate_text_via_aws
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(source_text, source_language, target_language):
    request = TranslationRequest(
        source_text=normalize_text(source_text),
        source_language=source_language,
        target_language=target_language,
    )
    translated = translate_text_via_aws(request.source_text, request.source_language, request.target_language)
    return TranslationResponse(translated, request.source_language, request.target_language, "aws.translate")
