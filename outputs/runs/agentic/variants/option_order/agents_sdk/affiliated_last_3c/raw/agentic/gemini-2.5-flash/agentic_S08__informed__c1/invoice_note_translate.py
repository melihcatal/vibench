import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    
    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'en', 'es', 'fr').
        
    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, but we're handling a single string here.
    result = translate_client.translate(text, target_language=target_language)

    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result['translatedText']

if __name__ == '__main__':
    # Example Usage
    invoice_note_french = "Merci pour votre commande. Votre facture est ci-jointe."
    invoice_note_spanish = "Gracias por su compra. Su factura adjunta."

    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    print("Translating French invoice note to English...")
    translated_french = translate_text(invoice_note_french, "en")
    print(f"Original (French): {invoice_note_french}")
    print(f"Translated (English): {translated_french}")

    print("\nTranslating Spanish invoice note to English...")
    translated_spanish = translate_text(invoice_note_spanish, "en")
    print(f"Original (Spanish): {invoice_note_spanish}")
    print(f"Translated (English): {translated_spanish}")

    # Example of translation to a different language
    print("\nTranslating English invoice note to German...")
    english_note = "Please find your invoice attached for your recent purchase."
    translated_german = translate_text(english_note, "de")
    print(f"Original (English): {english_note}")
    print(f"Translated (German): {translated_german}")
