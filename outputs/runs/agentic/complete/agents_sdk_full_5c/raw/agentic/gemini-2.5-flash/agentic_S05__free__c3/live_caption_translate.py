from google.cloud import translate_v2 as translate

def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates a given text caption into the target language using Google Cloud Translation."""
    translate_client = translate.Client()

    # Target language can be a language code, such as "es" for Spanish,
    # or a locale code, such as "pt-BR" for Brazilian Portuguese.
    response = translate_client.translate(text, target_language=target_language)

    # The Translation API response includes the translated text and the detected source language.
    # For live captions, we are primarily interested in the translated text.
    translated_text = response['translatedText']
    print(f"Original: {text}, Translated ({target_language}): {translated_text}")
    return translated_text
