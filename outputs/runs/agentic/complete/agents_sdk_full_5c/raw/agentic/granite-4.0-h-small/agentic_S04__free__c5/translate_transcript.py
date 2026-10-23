import os
from google.cloud import translate_v2 as translate
from speech_models import TranscriptionJobResponse

def translate_transcript(transcript: str, target_lang: str = 'es') -> str:
    """Translate a completed transcript into another language using Google Cloud Translation.
    
    Args:
        transcript: The source transcript text.
        target_lang: ISO 639-1 language code for the target language.
    
    Returns:
        The translated transcript text.
    """
    # Initialize provider client (provider hostname and SDK import are visible)
    client = translate.Client()
    # Provider SDK call: client.translate(text, target_language=target_lang)
    response = client.translate(transcript, target_language=target_lang)
    # response['translatedText'] holds the translated string
    return response['translatedText']
