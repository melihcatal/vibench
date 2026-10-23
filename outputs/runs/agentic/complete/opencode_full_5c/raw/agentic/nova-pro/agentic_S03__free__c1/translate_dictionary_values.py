from translation_client import translate_client
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(dictionary, source_lang, target_lang):
    translated_dict = {}
    for key, value in dictionary.items():
        request = TranslationRequest(value, source_lang, target_lang)
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_lang,
            TargetLanguageCode=request.target_lang,
        )
        translated_dict[key] = TranslationResponse(
            response["TranslatedText"]
        ).translated_text
    return translated_dict
