from google.cloud import translate_v2 as translate
from identity_models import TranslateRequest, TranslateResponse
import os

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    client = translate.Client()
    try:
        result = client.translate(request['text'], target_language=request['target_language'])
        return {"translated_text": result['translatedText']}
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {e}")

