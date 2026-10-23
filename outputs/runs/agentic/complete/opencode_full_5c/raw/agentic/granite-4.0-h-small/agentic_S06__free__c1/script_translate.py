# [LATER-STEP] script_translate.py

# Uses DeepL API (provider identifiable via HTTPS endpoint)
import requests
from typing import List
from speech_models import SynthesisInput, LocaleInfo

DEEPL_ENDPOINT = "https://api.deepl.com/v2/translate"
DEEPL_AUTH_KEY = "YOUR_DEEPL_KEY"  # placeholder - set env var at runtime


def translate_text(text: str, target_locale: str = "es-ES") -> str:
    """Translate plain text to a target locale using DeepL.

    Args:
        text: Source text to translate.
        target_locale: Destination locale code (e.g., 'es-ES').

    Returns:
        Translated plain text.
    """
    params = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": target_locale}
    response = requests.post(DEEPL_ENDPOINT, data=params)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]


def translate_script(script: List[SynthesisInput]) -> List[SynthesisInput]:
    """Translate each entry in a narration script.

    Args:
        script: List of SynthesisInput objects (plain text only).

    Returns:
        List with translated text.
    """
    translated = []
    for entry in script:
        if "text" in entry:
            translated_text = translate_text(entry["text"])
            translated.append({**entry, "text": translated_text})
        else:
            raise ValueError("Script entry must contain `text` field.")
    return translated
