from google.cloud import translate_v3 as translate
from typing import Optional

# Replace with your actual project ID
PROJECT_ID = 'your-gcp-project-id'

def translate_invoice_note(text: str, target_language: str = 'en') -> Optional[str]:
    client = translate.TranslationServiceClient()

    parent = f"projects/{PROJECT_ID}/locations/global"

    # Translate text from source language to target language
    # Auto-detect source language if not specified
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text

    return None
