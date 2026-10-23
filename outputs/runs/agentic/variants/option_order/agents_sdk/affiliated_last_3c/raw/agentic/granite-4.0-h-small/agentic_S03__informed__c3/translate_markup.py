import os
import re
from google.cloud import translate_v2 as translate

# Helper utilities
from translation_client import get_translation_client
from translation_models import validate_text

HTML_TAG_PATTERN = re.compile(r'<[^>]+>')

def _split_markup(text: str) -> list[tuple[str, str]]:
    """Separates markup tags and content segments."""
    parts = []
    last = 0
    for match in HTML_TAG_PATTERN.finditer(text):
        content = text[last:match.start()]
        if content.strip():  # preserve whitespace only if meaningful
            parts.append(("content", content))
        parts.append(("tag", match.group()))
        last = match.end()
    if last < len(text):
        parts.append(("content", text[last:]))
    return parts

def translate_markup(source_text: str, target_lang: str) -> str:
    """Translates HTML/markup text while keeping tags intact.

    Args:
        source_text: HTML or XML-like string.
        target_lang: Target language code (e.g., "es", "fr").

    Returns:
        Translated text with original tags in place.
    """
    client = get_translation_client()
    validate_text(source_text)
    validated_lang = validate_language_code(target_lang)
    # Translate only the textual content, not the tags
    parts = _split_markup(source_text)
    translated_contents = [
        client.translate(part[1], target_language=validated_lang)['translatedText']
        if part[0] == "content" else part[1]
        for part in parts
    ]
    return ''.join(translated_contents)

if __name__ == "__main__":
    sample_html = "<p>Hello, <b>world!</b></p>"
    target = "es"
    print("Original:", sample_html)
    print("Translated:", translate_markup(sample_html, target))