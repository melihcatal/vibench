import os
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translates a query into a target language using Google Cloud Translation.
    Authentication typically uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    translate_client = translate.Client()

    response = translate_client.translate(
        query,
        target_language=target_language,
        model="nmt" # Use Neural Machine Translation model
    )

    translated_text = response["translatedText"]
    print(f"Original: {query}")
    print(f"Translated to {target_language}: {translated_text}")
    print(f"Detected source language: {response['detectedSourceLanguage']}")
    
    return translated_text

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set to a path to your service account key file
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    
    german_query = "Wie geht es Ihnen heute?"
    spanish_query = "¿Cuál es el pronóstico del tiempo?"

    translated_german = translate_query(german_query, target_language="en")
    translated_spanish = translate_query(spanish_query, target_language="en")

    print(f"Translated German query: {translated_german}")
    print(f"Translated Spanish query: {translated_spanish}")
