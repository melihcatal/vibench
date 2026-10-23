import os
from typing import List
from google.cloud import translate

# Google Cloud Translation Configuration
GOOGLE_CLOUD_PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')

def translate_text_segments(text_segments: List[str], target_language_code: str = 'es') -> List[str]:
    if not GOOGLE_CLOUD_PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{GOOGLE_CLOUD_PROJECT_ID}/locations/global"

    translated_texts = []
    for text in text_segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts