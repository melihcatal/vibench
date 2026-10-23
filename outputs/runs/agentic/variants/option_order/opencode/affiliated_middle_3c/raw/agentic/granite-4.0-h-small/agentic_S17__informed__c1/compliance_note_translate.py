import os
from google.cloud.translate_v3 import TranslationServiceClient
from security_models import EncryptRequest

# Translate encryption or compliance notes for reviewer consumption


def translate_note(text: str, target_lang: str = "es") -> str:
    """Translate given text to target language using Google Cloud Translation API."""
    client = TranslationServiceClient()
    parent = f"projects/{os.getenv('GCP_PROJECT_ID')}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_lang,
        }
    )
    translated = response.translations[0].translated_text
    return translated.strip()


if __name__ == "__main__":
    sample = "The key must be rotated every 90 days per compliance policy."
    translated = translate_note(sample, target_lang="fr")
    print("Translated note:", translated)
