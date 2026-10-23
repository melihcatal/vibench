import os
from google.cloud import translate_v2 as translate

# Google Gemini translation (later-step)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
translator = translate.Client()


def translate_appeal(text: str, target_lang: str = "en") -> str:
    """Translates an appeal message for reviewer consumption.

    Args:
        text (str): Original appeal text (any language).
        target_lang (str): Target language code (default "en").

    Returns:
        str: Translated appeal in target language.
    """
    response = translator.translate(text, target_language=target_lang)
    return response["translatedText"]
