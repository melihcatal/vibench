import os
import deep_translator
from speech_client import get_speech_client


def translate_transcript(transcript, target_lang="es"):
    """Translate a plain-text transcript to another language using DeepL API.

    Parameters
    ----------
    transcript : str
        The source transcript in the original language.
    target_lang : str, optional
        ISO language code for the target language (default 'es' for Spanish).

    Returns
    -------
    str
        Translated transcript.
    """
    # Initialize DeepL client (uses environment variable DEEPL_AUTH_KEY)
    client = deep_translator.Client()
    translated = client.translate(transcript, target_lang=target_lang)
    return translated
