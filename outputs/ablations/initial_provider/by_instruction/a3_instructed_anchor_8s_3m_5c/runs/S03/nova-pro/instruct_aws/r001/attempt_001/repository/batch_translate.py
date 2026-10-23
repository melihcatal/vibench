from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def batch_translate(texts, source_lang, target_lang):
    client = get_translate_client()
    results = []
    for text in texts:
        request = TranslationRequest(text, source_lang, target_lang)
        response = client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_lang,
            TargetLanguageCode=request.target_lang
        )
        results.append(TranslationResponse(response['TranslatedText']))
    return results