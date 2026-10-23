from google.cloud import translate_v2 as translate
from speech_models import TranslationRequest, TranslationResult

def translate_transcript(request: TranslationRequest) -> TranslationResult:
    client = translate.Client()
    result = client.translate(
        request.text,
        target_language=request.target_language_code,
        source_language=request.source_language_code,
    )
    return TranslationResult(
        translated_text=result["translatedText"],
        detected_language_code=result.get("detectedSourceLanguage"),
    )
