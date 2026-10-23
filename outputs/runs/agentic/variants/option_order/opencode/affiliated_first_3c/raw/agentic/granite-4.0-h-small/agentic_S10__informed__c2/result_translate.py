import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate generated model output to a target language using Google Cloud Translation."""
    api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not api_key:
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS env var with path to credentials"
        )
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]
