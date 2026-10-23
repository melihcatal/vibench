import os
from typing import Dict
from text_translation import TranslateText


def translate_consent_copy(
    consent_text: str, target_lang: str = "es"
) -> Dict[str, str]:
    """Translate identity‑provider consent copy into a target language.

    Uses DeepL translation service as the concrete provider.
    Returns a dict with the original text and the translated version.
    """
    translator = TranslateText(provider="deepl", target_lang=target_lang)
    translated = translator.translate(text=consent_text)
    return {
        "original": consent_text,
        "target_language": target_lang,
        "translated": translated,
    }


# Example usage (when presenting consent UI)
# consent_en = fetch_consent_from_provider()
# translated = translate_consent_copy(consent_en, "fr")
# print(translated['translated'])
