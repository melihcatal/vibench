import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    runbook_note_en = "Follow the quarterly secret rotation procedure for production databases."
    target_lang_es = "es"
    target_lang_fr = "fr"

    try:
        print(f"Original (EN): {runbook_note_en}")

        translated_es = translate_text(runbook_note_en, target_lang_es)
        print(f"Translated (ES): {translated_es}")

        translated_fr = translate_text(runbook_note_en, target_lang_fr)
        print(f"Translated (FR): {translated_fr}")

    except Exception as e:
        print(f"Error translating text: {e}")
