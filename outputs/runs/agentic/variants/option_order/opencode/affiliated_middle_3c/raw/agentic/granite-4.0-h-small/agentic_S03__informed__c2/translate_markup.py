# Python code for translate_markup.py
import os
import re
from typing import Dict

from translation_client import GeneralTextTranslationClient

TAG_PATTERN = re.compile(r"(</?[^>]+>)")


def translate_markup(
    markup: str,
    source_lang: str = "en",
    target_lang: str = "zh",
    **kwargs,
) -> Dict:
    """Translate HTML/markup while preserving tag structure.

    Args:
        markup (str): HTML/markup string.
        source_lang (str): Source language code.
        target_lang (str): Target language code.
        **kwargs: Additional provider-specific arguments.

    Returns:
        Dict: Result containing translated text with original markup preserved.
    """
    client = GeneralTextTranslationClient()
    # Split into tags and text nodes
    parts = TAG_PATTERN.split(markup)
    translated_parts = []
    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            # Preserve tag unchanged
            translated_parts.append(part)
        else:
            # Translate text node
            translated = client.translate(
                texts=[part],
                source_lang=source_lang,
                target_lang=target_lang,
                **kwargs,
            )[0]
            translated_parts.append(translated["translatedText"])
    translated_html = "".join(translated_parts)
    return {
        "inputMarkup": markup,
        "translatedMarkup": translated_html,
    }
