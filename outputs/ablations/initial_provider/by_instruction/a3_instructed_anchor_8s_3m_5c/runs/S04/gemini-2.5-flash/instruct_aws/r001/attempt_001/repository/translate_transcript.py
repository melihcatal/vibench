from google.cloud import translate_v2 as translate
from speech_models import TranslationRequest
import os

def translate_text_segment(request: TranslationRequest) -> str:
    # Google Cloud Translation API
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    translate_client = translate.Client()
    
    result = translate_client.translate(
        request.text,
        source_language=request.source_language,
        target_language=request.target_language
    )
    return result['translatedText']
