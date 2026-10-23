from google.cloud import translate_v2 as translate
from storage_models import TranslateTextRequest


def stored_text_translate(request: TranslateTextRequest):
    client = translate.Client()
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
    }
