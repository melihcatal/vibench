from translation_client import translate_text_html_via_aws
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_markup(source_markup, source_language, target_language):
    request = TranslationRequest(normalize_text(source_markup), source_language, target_language)
    translated = translate_text_html_via_aws(request.source_text, request.source_language, request.target_language)
    return TranslationResponse(translated, request.source_language, request.target_language, "aws.translate")
