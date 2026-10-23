from translation_client import get_translate_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_response,
)


def translate_dictionary_values(dictionary, source_lang, target_lang):
    client = get_translate_client()
    translated_dict = {}
    for key, value in dictionary.items():
        request = TranslationRequest(value, source_lang, target_lang)
        response = client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_lang,
            TargetLanguageCode=request.target_lang,
        )
        translated_dict[key] = normalize_response(response).translated_text
    return translated_dict
