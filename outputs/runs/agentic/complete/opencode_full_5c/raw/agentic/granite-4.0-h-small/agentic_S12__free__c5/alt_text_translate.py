# LATER-STEP
# Translate generated image descriptions to another language using Google Translate API
import json
from google.cloud import translate_v2 as translate


def translate_description(source_text: str, target_lang: str = "es") -> str:
    """Translate a short image caption to the target language.

    Args:
        source_text: The original image caption.
        target_lang: ISO language code (default Spanish 'es').

    Returns:
        Translated caption.
    """
    client = translate.Client()
    result = client.translate(source_text, target_language=target_lang)
    return result["translatedText"]
