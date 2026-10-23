from google.cloud import translate_v2 as translate
import os


def translate_compliance_note(text: str, target_language: str) -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.
    
    Args:
        text: The compliance note to translate.
        target_language: The target language code (e.g., 'es', 'fr').
    
    Returns:
        The translated text.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    
    client = translate.Client()
    
    result = client.translate(
        text,
        target_language=target_language
    )
    
    return result['translatedText']