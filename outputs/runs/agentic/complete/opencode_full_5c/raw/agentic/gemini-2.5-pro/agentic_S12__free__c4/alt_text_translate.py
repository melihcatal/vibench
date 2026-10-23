from google.cloud import translate_v2 as translate
from vision_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """Translates text to a target language using Google Cloud Translate."""
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text, target_language=request.target_language
    )

    return TranslationResponse(translated_text=result["translatedText"])
