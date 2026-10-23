import os
from google.cloud import translate_v2 as translate

def translate_narration(script_text, target_locale='en-US'):
    """Translate a narration script into the target locale using Google Cloud Translation.
    Args:
        script_text (str): Original narration text.
        target_locale (str): BCP-47 code, e.g., 'es-ES', 'fr-FR'.
    Returns:
        str: Translated script.
    """
    translator = translate.Client()
    result = translator.translate(script_text, target_language=target_locale)
    return result['translatedText']
