# script_translate.py
# [LATER-STEP] Translate narration scripts before synthesis using Google Cloud Translation API.

from google.cloud import translate_v2 as translate
from speech_client import get_texttospeech_client  # reused for credentials handling

def translate_script(script: str, target_language: str = 'es') -> str:
    """Translate a narration script to a target language.

    Args:
        script: Plain text or SSML script.
        target_language: BCP-47 language code (default: 'es' Spanish).

    Returns:
        Translated script ready for synthesis.
    """
    client = translate.Client()  # Uses same ADC sources as TTS client
    result = client.translate(script, target_language=target_language)
    # Return translated text; preserve SSML tags by translating only non-tag content if needed
    return result['translatedText']
