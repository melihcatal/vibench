import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        model='nmt' # Neural Machine Translation model
    )
    return result['translatedText']

if __name__ == '__main__':
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    translated_string = translate_text("Hello World", "fr")
    print(f"Translated: {translated_string}")
