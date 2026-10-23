import os
from deepl import DeepL

def translate_narration(script_text: str, target_lang: str = 'en') -> str:
    """Translate a narration script using DeepL API.
    The default target language is English ('en').
    """
    # Ensure the environment variable for DeepL auth is set
    api_key = os.getenv('DEEPL_AUTH_KEY')
    if not api_key:
        raise RuntimeError('Missing DEEPL_AUTH_KEY environment variable')
    translator = DeepL.Translator(api_key)
    translation = translator.translate_text(script_text, target_lang=target_lang)
    return translation.text
