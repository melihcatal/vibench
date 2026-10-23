"""
Translates a single text string between languages.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from typing import Optional

from translation_client import get_client
from translation_models import TranslationResult


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    """
    Translate a single text string from source_lang to target_lang.

    Args:
        text: The text string to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Source language code (optional; DeepL auto-detects if omitted).
        formality: Formality level ('prefer_more' or 'prefer_less'; optional).

    Returns:
        TranslationResult containing the translated text and metadata.
    """
    client = get_client()
    result = client.translate(
        text=text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )
    return result


if __name__ == "__main__":
    result = translate_text("Hello, world!", target_lang="DE")
    print(result)
