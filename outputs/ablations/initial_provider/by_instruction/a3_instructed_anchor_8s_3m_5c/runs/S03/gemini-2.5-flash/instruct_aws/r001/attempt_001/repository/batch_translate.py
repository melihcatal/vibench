from google.cloud import translate_v2 as translate
import os
from translation_models import BatchTranslationRequest, BatchTranslationResponse

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

def batch_translate_google(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = translate.Client()
    translated_texts = []
    for text in request.texts:
        result = client.translate(text, source_language=request.source_language, target_language=request.target_language)
        translated_texts.append(result['translatedText'])
    return BatchTranslationResponse(translated_texts, request.source_language, request.target_language)
