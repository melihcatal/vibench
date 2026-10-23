import os
from google.cloud import translate_v2 as translate

def translate_note(text: str, target_language: str = "es") -> str:
    """
    Translates a metric or dashboard note to another locale using Google Cloud Translate.
    """
    # This authenticates via GOOGLE_APPLICATION_CREDENTIALS env var
    # which is a provider-specific signal.
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    
    return result["translatedText"]

if __name__ == '__main__':
    note_en = "Alert: High CPU utilization detected on production servers."
    target_locale = "fr" # French

    try:
        print(f"Original (en): {note_en}")
        translated_note = translate_note(note_en, target_locale)
        print(f"Translated ({target_locale}): {translated_note}")

        note_es = "El uso de la memoria ha superado el 90%."
        target_locale_en = "en"
        print(f"\nOriginal (es): {note_es}")
        translated_note_en = translate_note(note_es, target_locale_en)
        print(f"Translated ({target_locale_en}): {translated_note_en}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Ensure you have authenticated with Google Cloud CLI (gcloud auth application-default login).")
