import os
import re
from translation_client import TranslationClient
from translation_models import GeneralMarkupRequest, GeneralMarkupResponse


def translate_markup(
    source_markup: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Translate HTML or markup while preserving tags.

    Args:
        source_markup: HTML or XML markup containing text content.
        source_lang: ISO language code for source (default "en").
        target_lang: ISO language code for target (default "es").

    Returns:
        Markup with translated text but original tag structure.
    """
    # Extract plain-text segments while preserving tag placeholders
    segments = []
    parts = re.split(r"(<[^>]+>)", source_markup)
    for part in parts:
        # If part is a tag, keep as-is; if text, translate
        if part.startswith("<") and part.endswith(">"):
            segments.append(part)
        else:
            # Translate plain text
            translated = translate_text(part, source_lang, target_lang)
            segments.append(translated)
    return "".join(segments)


# Helper that reuses translate_text from same-scenario file
from translate_text import translate_text
