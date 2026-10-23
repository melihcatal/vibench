import os
from google.cloud import translate_v2 as translate
from speech_models import TranslatedSegment

def translate_transcript(text: str, target_language: str, source_language: str = 'en') -> TranslatedSegment:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # or provide credentials explicitly if not running in a Google Cloud environment
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        # Placeholder for explicit credential setup if needed outside GCE/Cloud Run
        # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.
        pass

    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    
    # The Translation API doesn't return segment_id, so we'll use a dummy one or infer if multiple segments are passed
    return TranslatedSegment(
        segment_id=0, # Assuming single segment for simplicity; extend if multi-segment required
        text=text,
        translated_text=result['translatedText'],
        source_language=result['detectedSourceLanguage'],
        target_language=target_language
    )
