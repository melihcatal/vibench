from identity_client import config
from identity_models import TranslateRequest, TranslateResponse

def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation API.
    """
    try:
        result = config.translate_client.translate(
            request.text,
            target_language=request.target_language,
            source_language=request.source_language
        )
        translated_text = result["translatedText"]
        detected_source_language = result.get("detectedSourceLanguage")

        return TranslateResponse(
            translated_text=translated_text,
            detected_source_language=detected_source_language
        )
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {e}")
