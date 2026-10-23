import os
from google.cloud import translate_v2 as translate

def translate_payload_text(text: str, target_language: str = "en", project_id: str = None) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation."""
    client = translate.Client(project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))

    # Text can also be a list of strings, in which case a list of translations is returned.
    # The Google Cloud Translation client automatically uses GOOGLE_APPLICATION_CREDENTIALS.
    result = client.translate(text, target_language=target_language)

    # The result is a dictionary with 'translatedText', 'detectedSourceLanguage', and 'input'
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var set)
    # from your shell, run:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python payload_translate.py
    french_text = "Bonjour le monde, comment allez-vous?"
    spanish_text = "Hola mundo, ¿cómo estás?"

    translated_to_english_french = translate_payload_text(french_text, "en")
    print(f"Original French: {french_text}")
    print(f"Translated to English: {translated_to_english_french}\n")

    translated_to_english_spanish = translate_payload_text(spanish_text, "en")
    print(f"Original Spanish: {spanish_text}")
    print(f"Translated to English: {translated_to_english_spanish}")
