import re
from .translate_text import translate_text


def translate_markup(
    source_markup: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Translate HTML or markup while preserving tags.

    The implementation extracts text nodes, translates them, and reassembles the markup.
    """
    # Simple regex to separate tags from text content
    parts = re.split(r"(</?[^>]+>)", source_markup)
    translated_parts = []
    for part in parts:
        if re.match(r"<[^/].*>", part):  # Opening or self-closing tag, keep as-is
            translated_parts.append(part)
        elif part.strip() == "":  # Empty string, keep as-is
            translated_parts.append(part)
        else:  # Text content, translate
            translated_parts.append(translate_text(part, source_lang, target_lang))
    return "".join(translated_parts)
