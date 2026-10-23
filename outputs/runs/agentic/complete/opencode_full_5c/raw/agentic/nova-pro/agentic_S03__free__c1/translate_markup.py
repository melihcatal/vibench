from translation_client import translate_client
from translation_models import TranslationRequest, TranslationResponse
import re


def translate_markup(markup, source_lang, target_lang):
    text = re.sub(r"<[^>]+>", "", markup)
    request = TranslationRequest(text, source_lang, target_lang)
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_lang,
        TargetLanguageCode=request.target_lang,
    )
    translated_text = response["TranslatedText"]
    translated_markup = re.sub(text, translated_text, markup)
    return translated_markup
