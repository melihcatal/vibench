import os
from google.cloud import translate_v2 as translate

# Configure Google Cloud Translation client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
def get_translate_client():
    return translate.Client()

def translate_payload_text(text: str, target_language: str, source_language: str = None) -> dict:
    """Translates customer-facing message payload text using Google Cloud Translation."""
    client = get_translate_client()

    try:
        # The target_language is the BCP-47 language code (e.g., "fr", "es", "ja")
        result = client.translate(text, target_language=target_language, source_language=source_language)

        translated_text = result['translatedText']
        detected_source_language = result['detectedSourceLanguage']

        print(f"Original text: {text}")
        print(f"Source language: {detected_source_language}")
        print(f"Target language: {target_language}")
        print(f"Translated text: {translated_text}")

        return {
            "success": True,
            "original_text": text,
            "translated_text": translated_text,
            "source_language": detected_source_language,
            "target_language": target_language
        }
    except Exception as e:
        return {"success": False, "error": f"Translation failed: {e}"}

if __name__ == "__main__":
    # Example usage
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # python payload_translate.py

    text_to_translate = "Hello, how are you?"
    target_lang = "es" # Spanish

    print(f"\nAttempting to translate '{text_to_translate}' to {target_lang}")
    translation_result = translate_payload_text(text_to_translate, target_lang)
    print(translation_result)

    text_to_translate_fr = "Bonjour, comment allez-vous?"
    target_lang_en = "en" # English

    print(f"\nAttempting to translate '{text_to_translate_fr}' to {target_lang_en}")
    translation_result_fr_en = translate_payload_text(text_to_translate_fr, target_lang_en)
    print(translation_result_fr_en)
