# welcome_translate.py
from google.cloud import translate_v2 as translate

def translate_welcome_message(text: str, target_language: str) -> str:
    """
    Translates a welcome message to the user's target language
    using Google Cloud Translation.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        text, 
        target_language=target_language,
        # Using a generic model for broad compatibility
        model=translate.NMT
    )

    return result['translatedText']
