import re
from translate_text import translate_text


def translate_markup(
    html: str, src_lang: str = GOOGLE_SOURCE_LANG, tgt_lang: str = GOOGLE_TARGET_LANG
) -> str:
    """
    Translates HTML/markup content while preserving tags.

    The function extracts text nodes, translates them, and reinserts the tags.

    Args:
        html: HTML string.
        src_lang: Source language code.
        tgt_lang: Target language code.

    Returns:
        HTML string with translated text content.
    """
    # Simple regex to separate tags from text (not a full HTML parser)
    parts = re.split(r"(</?[^>]+>)", html)
    translated_parts = []
    for part in parts:
        # Preserve tags unchanged
        if part.startswith("<") and part.endswith(">"):
            translated_parts.append(part)
        else:
            translated = translate_text(part, src_lang, tgt_lang)
            translated_parts.append(translated)
    return "".join(translated_parts)
