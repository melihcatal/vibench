import os
from google.cloud import translate_v2 as translate

def batch_translate(texts: list[str], target_language: str, source_language: str = None) -> list[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation."""
    client = translate.Client()
    results = client.translate(
        texts,
        target_language=target_language,
        source_language=source_language,
        model='nmt' # Neural Machine Translation model
    )
    return [result['translatedText'] for result in results]

if __name__ == '__main__':
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    texts_to_translate = ["Hello", "World"]
    translated_texts = batch_translate(texts_to_translate, "es")
    print(f"Translated list: {translated_texts}")
