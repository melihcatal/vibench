import html
import re
from translate_text import translate_text
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    NormalizedTranslation,
)

PROVIDER_NAME = "deepl"

# Regex to capture HTML tags so they are not sent to the translation engine
TAG_REGEX = re.compile(r"(<[^>]+>)")


async def translate_markup(
    markup: str, target_lang: str, source_lang: str = "auto"
) -> str:
    """Translate HTML or markup while preserving tags and tag order.",
    Splits the input into tags and text nodes, translates only the text nodes, and
    reassembles the final string.
    """
    parts = TAG_REGEX.split(markup)  # alternates tag, text, tag, text ...
    translated_parts = []
    for part in parts:
        if TAG_REGEX.match(part):
            # Leave tags untouched
            translated_parts.append(part)
        else:
            # Translate only text nodes
            translated = await translate_text(part, target_lang, source_lang)
            translated_parts.append(translated)
    return "".join(translated_parts)
