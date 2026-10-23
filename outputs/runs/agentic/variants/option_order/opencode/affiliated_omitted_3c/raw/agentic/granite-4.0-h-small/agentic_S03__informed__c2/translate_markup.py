import os
import re
from translate_text import translate_text

# Alibaba Machine Translation example
# Uses translate_text helper which already configures the Alibaba SDK


def translate_markup(
    text: str,
    source_lang: str = "en",
    target_lang: str = "zh",
    preserve_tags: bool = True,
) -> str:
    """Translate HTML/markup text while preserving tags.

    The function extracts tag content, translates it, and re‑injects the tags.
    This simplistic approach works for well‑formed HTML fragments.

    Args:
        text: Source markup string.
        source_lang: Language code of the source text.
        target_lang: Language code of the target language.
        preserve_tags: If True (default) ensures markup tags remain unchanged.

    Returns:
        Translated text with original markup retained.
    """
    # Regex to split on HTML tags, keeping tags in capture groups
    tag_pattern = re.compile(r"(<[^>]+>)")
    parts = tag_pattern.split(text)
    translated_parts = []

    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            # Preserve tag as‑is
            translated_parts.append(part)
        else:
            # Translate only non‑tag content
            translated_parts.append(translate_text(part, source_lang, target_lang))

    return "".join(translated_parts)


# Simple demo when run directly
if __name__ == "__main__":
    sample_html = "<p>Hello, <strong>world!</strong></p>"
    print("Original:", sample_html)
    print("Translated:", translate_markup(sample_html))
