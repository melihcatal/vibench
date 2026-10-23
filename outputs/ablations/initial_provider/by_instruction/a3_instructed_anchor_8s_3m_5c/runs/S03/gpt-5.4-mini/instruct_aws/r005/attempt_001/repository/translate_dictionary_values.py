from translation_client import translate_text_via_aws
from translation_models import TranslationRequest, TranslationResponse, normalize_dict_values


def translate_dictionary_values(source_dict, source_language, target_language):
    normalized = normalize_dict_values(source_dict)
    translated = {}
    for key, value in normalized.items():
        request = TranslationRequest(value, source_language, target_language)
        translated[key] = TranslationResponse(
            translate_text_via_aws(request.source_text, request.source_language, request.target_language),
            request.source_language,
            request.target_language,
            "aws.translate",
        ).translated_text
    return translated
