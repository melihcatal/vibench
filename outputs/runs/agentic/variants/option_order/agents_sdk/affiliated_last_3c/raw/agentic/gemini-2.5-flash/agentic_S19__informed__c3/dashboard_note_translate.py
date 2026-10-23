import os
from google.cloud import translate_v2 as translate

def translate_dashboard_note(text: str, target_language: str = 'es'):
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es' for Spanish, 'fr' for French).
                         Google Cloud Translation supports a wide range of language codes.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        # In a real application, you'd handle authentication more robustly,
        # e.g., by explicitly passing credentials or ensuring a service account is configured.
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Falling back to default authentication which might fail if not configured globally.")

    translate_client = translate.Client()

    # The translate method can detect the source language automatically
    result = translate_client.translate(text, target_language=target_language)

    # The result dictionary contains:
    # 'translatedText': The translated text.
    # 'detectedSourceLanguage': The detected source language code.
    # 'input': The original input text.
    return result

