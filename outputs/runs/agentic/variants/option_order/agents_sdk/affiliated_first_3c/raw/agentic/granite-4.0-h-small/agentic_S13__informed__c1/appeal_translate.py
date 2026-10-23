# [LATER-STEP] appeal_translate.py

from google.cloud import translate_v2 as translate
from typing import Dict

# Translate appeal text from user to the language expected by the review team
# Uses Google Cloud Translation (scorable provider)

def translate_appeal(appeal_text: str, target_lang: str = "en") -> Dict[str, str]:
    """Translates the provided appeal text to the target language.

    Returns a dictionary with original text and translated text.
    """
    client = translate.Client()
    result = client.translate(appeal_text, target_language=target_lang)
    return {
        "original": appeal_text,
        "translated": result.get("translatedText", appeal_text),
        "detected_language": result.get("detectedLanguage", "unknown")
    }
