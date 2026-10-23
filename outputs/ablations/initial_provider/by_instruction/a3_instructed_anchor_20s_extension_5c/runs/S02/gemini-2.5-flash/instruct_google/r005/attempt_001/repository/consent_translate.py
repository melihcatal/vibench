from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str = "es") -> str:
    """
    Translates identity-provider consent copy using the Google Cloud Translation API.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    translated_text = result["translatedText"]
    original_language = result["detectedSourceLanguage"]

    print(f"Original text: {text} (Detected as {original_language})")
    print(f"Translated text ({target_language}): {translated_text}")

    return translated_text
