from google.cloud import translate_v2 as translate
from speech_models import TranslateRequest, TranslateResult

def translate_transcript(request: TranslateRequest) -> TranslateResult:
    """Translate completed transcript segments using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(
        request.text,
        target_language=request.target_language,
        model="nmt",
    )
    return TranslateResult(translated_text=result["translatedText"])