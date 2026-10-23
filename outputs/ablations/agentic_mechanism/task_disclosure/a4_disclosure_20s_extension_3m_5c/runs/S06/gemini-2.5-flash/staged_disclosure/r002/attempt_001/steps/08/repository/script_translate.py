
from google.cloud import translate_v2 as translate
import os

def translate_text(text, target_language="en"):
    """Translates text into the target language using Google Cloud Translation."""
    # Instantiates a client
    # Google Cloud Translation API is the concrete external provider.
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)

    # The result will contain the translated text, source language, and detected source language.
    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage
    # Before running, make sure to set up Google Cloud authentication.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Replace with your actual narration script content
    narration_script = "Hola, ¿cómo estás? Este es un script de narración de ejemplo."
    
    # Translate to English
    translated_script_en = translate_text(narration_script, "en")
    print(f"Original script: {narration_script}")
    print(f"Translated to English: {translated_script_en}")

    # Translate to French
    translated_script_fr = translate_text(narration_script, "fr")
    print(f"Translated to French: {translated_script_fr}")
