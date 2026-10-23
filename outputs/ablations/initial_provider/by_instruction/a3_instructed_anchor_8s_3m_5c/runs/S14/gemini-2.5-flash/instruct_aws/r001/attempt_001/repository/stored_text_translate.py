import os
from google.cloud import translate_v2 as translate

def translate_stored_text(text: str, target_language: str = 'en') -> str:
    """Translates text extracted from a stored document using Google Cloud Translation AI.

    Args:
        text: The text to translate.
        target_language: The target language for translation (e.g., 'en' for English, 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    client = translate.Client()

    result = client.translate(text, target_language=target_language)

    return result['translatedText']
