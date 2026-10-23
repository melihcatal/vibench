import os
from google.cloud import translate_v2 as translate
from google.cloud import storage

def get_translate_client():
    """Returns a Google Cloud Translation client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return translate.Client()

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    if not text:
        return ""

    client = get_translate_client()

    try:
        result = client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"Error translating text: {e}")
        return f"Translation failed: {text}"

if __name__ == '__main__':
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    #
    # spanish_note = "El cliente pidió una entrega rápida."
    # translated_note = translate_invoice_note(spanish_note, target_language="en")
    # print(f"Original: {spanish_note}")
    # print(f"Translated: {translated_note}")
    #
    # german_note = "Lieferung ist morgen fällig."
    # translated_note_de = translate_invoice_note(german_note, target_language="en")
    # print(f"Original: {german_note}")
    # print(f"Translated: {translated_note_de}")
    pass
