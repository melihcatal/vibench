# translate_markup.py
from translation_client import get_client
import re


def translate_markup(source_markup: str, source_lang: str, target_lang: str) -> str:
    """Translate HTML or markup while preserving tags using the configured provider."""
    # Extract and temporarily replace tag content to avoid translating inside tags
    tag_pattern = re.compile(r"<([^>]+)>([^<]+)</\\1>")
    placeholders = {}

    def replace_tag(m):
        key = f"__TAG{len(placeholders)}__"
        placeholders[key] = m.group(2)
        return key

    placeholder_text = tag_pattern.sub(replace_tag, source_markup)
    # Translate the text without tags
    translated_text = translate_text(placeholder_text, source_lang, target_lang)

    # Restore original tag content
    def restore_tag(m):
        key = m.group(0)
        return f"<{m.group(1)}>{placeholders[key]}</{m.group(1)}>"

    return tag_pattern.sub(restore_tag, translated_text)


# Helper imports local translation_text for re-use
from .translate_text import translate_text
