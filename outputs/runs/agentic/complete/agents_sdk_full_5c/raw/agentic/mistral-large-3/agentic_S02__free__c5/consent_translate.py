from google.cloud import translate_v2 as translate
from typing import Dict

def translate_consent_text(text: str, target_language: str, credentials_path: str) -> Dict:
    client = translate.Client.from_service_account_json(credentials_path)
    result = client.translate(
        text,
        target_language=target_language,
        source_language='en',
        format_='text',
    )
    return {
        'translated_text': result['translatedText'],
        'detected_source_language': result['detectedSourceLanguage'],
    }