from identity_client import IdentityClient
from identity_models import TranslateRequest, TranslateResponse

def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    client = IdentityClient()

    if not client.google_translation_client:
        raise ValueError("Google Cloud Translation client not configured.")

    try:
        result = client.google_translation_client.translate(
            request.text, target_language=request.target_language, source_language=request.source_language
        )

        translated_text = result["translatedText"]
        return TranslateResponse(translated_text=translated_text)
    except Exception as e:
        raise RuntimeError(f"Google Cloud Translation failed: {e}")
