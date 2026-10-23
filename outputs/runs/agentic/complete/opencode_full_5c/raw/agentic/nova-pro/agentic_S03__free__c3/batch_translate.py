from translation_client import get_translate_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_response,
)


def batch_translate(texts, source_lang, target_lang):
    client = get_translate_client()
    translated_texts = []
    for text in texts:
        request = TranslationRequest(text, source_lang, target_lang)
        response = client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_lang,
            TargetLanguageCode=request.target_lang,
        )
        translated_texts.append(normalize_response(response).translated_text)
    return translated_texts
